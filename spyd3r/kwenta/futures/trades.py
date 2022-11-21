import json
import websockets
from web3 import Web3
from loguru import logger
from eth_abi import decode_abi

from link import pubsub, synchroniser

from .markets import Kwenta_Futures_Markets

from spyd3r.helpers import restart_on_failure

from env import WEB3_NODE


class Kwenta_Futures_Trades:

    markets = Kwenta_Futures_Markets()
    topic_pubsub = "kwenta_futures:trades"

    async def initialise(self):
        await self.connect()
        await self.subscribe()
        synchroniser.set(event="kwenta_futures_trades")

    async def connect(self):
        url = WEB3_NODE.replace("https", "wss")
        self.ws = await websockets.connect(url)

    def construct_payload(self, address):
        return {
                "id": 1,
                "method": "eth_subscribe",
                "params": [
                    "logs",
                    {
                        "address": address,
                        "topics": ["0x930fd93131df035ac630ef616ad4212af6370377bf327e905c2724cd01d95097"],
                    },
                ],
            }

    async def subscribe(self):
        for address in self.markets.address_to_market.keys():
            await self.ws.send(json.dumps(self.construct_payload(address)))

    @restart_on_failure
    async def start(self):
        await self.initialise()

        while True:
            match json.loads(await self.ws.recv()):
                case {"params": {"result": {"address": address_contract, "topics": [_, _, address_hex], "data": data}}}:
                    # Decoding the data
                    data = bytes.fromhex(data[2:])
                    data = decode_abi(["uint256", "int256", "int256", "uint256", "uint256", "uint256"], data)

                    # Publishing the update
                    message = {
                        "market": self.markets.address_to_market[Web3.toChecksumAddress(address_contract)],
                        "account": Web3.toChecksumAddress(f"0x{address_hex[26:]}"),
                        "position": data[1] / 1e18,
                        "size": data[2] / 1e18,
                        "price": data[3] / 1e18,
                        "fees": data[5] / 1e18,
                    }
                    pubsub.send(topic=self.topic_pubsub, message=message)
                case {'id': _, 'result': _, 'jsonrpc': '2.0'}:
                    pass
                case payload:
                    logger.debug(payload)
