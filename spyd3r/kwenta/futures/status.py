import json
import websockets
from loguru import logger

from link import pubsub, synchroniser
from spyd3r.helpers import restart_on_failure

from env import WEB3_NODE


def parse_market_key(key: str):
    """
    Convert the hex market key to standardised human readable market string
    """
    market = bytes.fromhex(key).decode('utf-8')
    market = market.replace("\x00", "")
    return market[1:] + "/USD"


class Synthetix_Status:

    topic_kwenta_futures = "kwenta_futures_status"
    address_contract = "0xE8c41bE1A167314ABAF2423b72Bf8da826943FFD"
    topics = {
        "FuturesMarketResumed": "0x250fcb5d34afaf9bc18ec9ca0bf709e0f2ecb8ae4d4a3a616c0bf54b2ddf53e6",
        "FuturesMarketSuspended": "0xcaa561b71353382b62092c429c14613b5db8f9c5f3a27cb51df16e51f350f8ca",
    }

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
                    "topics": [self.topics["FuturesMarketSuspended"]],
                },
            ],
        }
        await self.ws.send(json.dumps(payload))

        payload = {
            "id": 2,
            "method": "eth_subscribe",
            "params": [
                "logs",
                {
                    "address": self.address_contract,
                    "topics": [self.topics["FuturesMarketResumed"]],
                },
            ],
        }
        await self.ws.send(json.dumps(payload))

    def parse_status(self, status: str):
        if status == self.topics["FuturesMarketSuspended"]:
            return "suspended"
        elif status == self.topics["FuturesMarketResumed"]:
            return "resumed"

        return ""

    @restart_on_failure
    async def start(self):
        await self.connect()
        await self.subscribe()
        synchroniser.set("kwenta_futures_market_status")

        while True:
            match json.loads(await self.ws.recv()):
                case {"params": {"event": {"topics": [status], "data": data}}}:
                    message = {
                        "market": parse_market_key(key=data[:66]),
                        "status": self.parse_status(status=status),
                    }
                    pubsub.send(topic=self.topic_kwenta_futures, message=message)
                case {'id': _, 'result': _, 'jsonrpc': '2.0'}:
                    pass
                case payload:
                    logger.debug(payload)
