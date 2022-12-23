import json
import websockets
from loguru import logger
from eth_abi import decode_abi

from link import pubsub, synchroniser
from spyd3r.helpers import restart_on_failure

from env import WEB3_NODE


class LIDO_stETH_Supply:

    address_contract = "0xae7ab96520de3a18e5e111b5eaab095312d7fe84"
    topic_event = "0x96a25c8ce0baabc1fdefd93e9ed25d8e092a3332f3aa9a41722b5697231d1d1a"
    topic_pubsub = "lido_steth_supply"

    async def connect(self):
        url = WEB3_NODE.replace("https", "wss")
        self.ws = await websockets.connect(url)

    async def subscribe(self):
        payload = {
            "id": 1,
            "method": "eth_subscribe",
            "params": [
                "logs",
                {
                    "address": self.address_contract,
                    "topics": [self.topic_event],
                },
            ],
        }
        await self.ws.send(json.dumps(payload))

    @restart_on_failure
    async def start(self):
        await self.connect()
        await self.subscribe()
        synchroniser.set("lido_steth_supply")

        while True:
            match json.loads(await self.ws.recv()):
                case {"params": {"result": {"topics": [_, address], "data": data}}}:
                    # Decoding the data
                    data = bytes.fromhex(data[2:])
                    data = decode_abi(["uint256", "address"], data)

                    # Publishing the update
                    message = {
                        "address": address,
                        "amount": data[0] / 1e18,
                    }
                    pubsub.send(topic=self.topic_pubsub, message=message)
                case {"id": _, "result": _, "jsonrpc": "2.0"}:
                    pass
                case payload:
                    logger.debug(payload)
