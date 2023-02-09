import json
import websockets
from loguru import logger

from spyd3r.helpers import restart_on_failure


class Logs:
    def __init__(self, rpc_endpoint: str, address: str, topic: str):
        self.rpc_endpoint = rpc_endpoint
        self.address = address
        self.topic = topic

    async def connect(self):
        url = self.rpc_endpoint.replace("https", "wss")
        self.ws = await websockets.connect(url)

    async def subscribe(self):
        payload = {
            "id": 1,
            "method": "eth_subscribe",
            "params": [
                "logs",
                {
                    "address": self.address,
                    "topics": [self.topic],
                },
            ],
        }
        await self.ws.send(json.dumps(payload))

    def process(self, tx_hash: str, topics: list, data):
        pass

    @restart_on_failure
    async def start(self):
        # Connecting and subscribing to the websocket
        await self.connect()
        await self.subscribe()

        while True:
            # Parsing the messages
            match json.loads(await self.ws.recv()):
                # Event
                case {
                    "params": {
                        "result": {
                            "address": _,
                            "topics": topics,
                            "data": data,
                            "transactionHash": tx_hash,
                        }
                    }
                }:
                    self.process(tx_hash, topics, data)
                # Connection
                case {"id": _, "result": _, "jsonrpc": "2.0"}:
                    pass
                # Others
                case payload:
                    logger.debug(payload)
