import json
import websockets
from loguru import logger
from eth_abi import decode_abi

from link import pubsub, synchroniser
from spyd3r.helpers import restart_on_failure

from env import WEB3_NODE


class LIDO_stETH_Transfer:

    address_contract = "0xae7ab96520de3a18e5e111b5eaab095312d7fe84"
    topic_event = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
    topic_pubsub = "lido_steth_transfer"

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
        synchroniser.set("lido_steth_transfer")

        while True:
            match json.loads(await self.ws.recv()):
                case {"params": {"result": {"topics": [_, address_from, address_to], "data": data}}}:
                    # Decoding the data
                    data = bytes.fromhex(data[2:])
                    data = decode_abi(["uint256"], data)

                    # Publishing the update
                    message = {
                        "from": address_from,
                        "to": address_to,
                        "amount": data[0] / 1e18,
                    }
                    pubsub.send(topic=self.topic_pubsub, message=message)
                case {"id": _, "result": _, "jsonrpc": "2.0"}:
                    pass
                case payload:
                    logger.debug(payload)
