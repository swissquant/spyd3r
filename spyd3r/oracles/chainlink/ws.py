import json
import websockets
from web3 import Web3
from loguru import logger

from link import pubsub, synchroniser

from .contract import fetch_aggregator_address

from spyd3r.helpers import restart_on_failure
from env import WEB3_NODE


class Oracle:

    aggregator_to_oracle: dict = {}
    topic_ws = "0x0559884fd3a460db3073b7fc896cc77986f16e378210ded43186175bf646fc5f"
    topic_pubsub = "chainlink:answer_updated"

    def __init__(self, oracles: dict[str, str]):
        """
        - oracles: map table of oracle name to its proxy addresse
        """
        self.oracles = oracles

    async def initialise(self):
        """
        Initialisie the module
        """
        # Initialising the aggregator addresses
        await self.initialise_aggregator_addresses()

        # Connecting and subscribing
        await self.connect()
        await self.subscribe()

        # Signalling that the websocket is ready
        synchroniser.set(event="chainlink_oracle")

    async def initialise_aggregator_addresses(self):
        """
        Construct the mapping table from aggregator to its associated oracle
        """
        if self.aggregator_to_oracle == {}:
            for oracle, address_proxy in self.oracles.items():
                address_aggregator = await fetch_aggregator_address(address=address_proxy)
                self.aggregator_to_oracle[address_aggregator] = oracle

    async def connect(self):
        """
        Connect to the websocket
        """
        url = WEB3_NODE.replace("https", "wss")
        self.ws = await websockets.connect(url)

    async def subscribe(self):
        """
        Subscribe to all the aggregator updates
        """
        id = 1
        for address_aggregator in self.aggregator_to_oracle.keys():
            payload = {
                "id": id,
                "method": "eth_subscribe",
                "params": [
                    "logs",
                    {
                        "address": address_aggregator,
                        "topics": [self.topic_ws],
                    },
                ],
            }
            await self.ws.send(json.dumps(payload))
            id += 1

    @restart_on_failure
    async def start(self):
        """
        Start the module
        """
        await self.initialise()

        while True:
            match json.loads(await self.ws.recv()):
                case {"params": {"result": {"topics": [_, answer_hex, _], "address": address_aggregator}}}:
                    message = {
                        "oracle": self.aggregator_to_oracle[Web3.toChecksumAddress(address_aggregator)],
                        "answer": int(answer_hex, 16) / 1e8
                    }
                    pubsub.send(topic="chainlink:answer_updated", message=message)
                case {'id': _, 'result': _, 'jsonrpc': '2.0'}:
                    pass
                case payload:
                    logger.debug(payload)
