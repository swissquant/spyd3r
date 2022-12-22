import json
import websockets
from loguru import logger
from eth_abi import decode_abi

from link import pubsub, synchroniser
from spyd3r.helpers import restart_on_failure

from env import WEB3_NODE


class LIDO_stETH_Rewards:

    address_contract = "0x442af784A788A5bd6F42A01Ebe9F287a871243fb"
    topic_event = "0xdafd48d1eba2a416b2aca45e9ead3ad18b84e868fa6d2e1a3048bfd37ed10a32"
    topic_pubsub = "lido_steth_rewards"

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
        synchroniser.set("lido_steth_rewards")

        while True:
            match json.loads(await self.ws.recv()):
                case {"params": {"event": {"data": data}}}:
                    # Decoding the data
                    data = bytes.fromhex(data[2:])
                    data = decode_abi(["uint256", "uint256", "uint256", "uint256"], data)

                    # Publishing the update
                    message = {
                        "eth_after": data[0] / 1e18,
                        "eth_before": data[1] / 1e18,
                        "time_elapsed": data[2],
                        "total_shares": data[3] / 1e18,
                    }
                    pubsub.send(topic=self.topic_pubsub, message=message)
                case {"id": _, "result": _, "jsonrpc": "2.0"}:
                    pass
                case payload:
                    logger.debug(payload)
