import json
import websockets

from link import pubsub

from spyd3r.helpers import restart_on_failure
from env import WEB3_NODE


class Web3_Transactions:

    topic = "web3:transactions"

    def __init__(self, silent: bool = True):
        self.silent = silent

    async def initialise(self):
        """
        Initialisie the module
        """
        # Connecting and subscribing
        await self.connect()
        await self.subscribe()

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
        payload = {
            "id": 1,
            "method": "eth_subscribe",
            "params": ["alchemy_minedTransactions"],
        }
        await self.ws.send(json.dumps(payload))

    @restart_on_failure
    async def start(self):
        """
        Start the module
        """
        await self.initialise()

        while True:
            match json.loads(await self.ws.recv()):
                case {
                    "jsonrpc": "2.0",
                    "method": "eth_subscription",
                    "params": {
                        "result": {
                            "transaction": {
                                "blockNumber": block_number,
                                "from": address_from,
                                "gas": gas,
                                "gasPrice": gas_price,
                                "maxFeePerGas": max_fee_per_gas,
                                "maxPriorityFeePerGas": max_priority_fee_per_gas,
                                "hash": tx_hash,
                                "input": data,
                                "nonce": nonce,
                                "to": address_to,
                                "value": value,
                            }
                        }
                    },
                }:
                    tx = {
                        "block_number": int(block_number, 16),
                        "from": address_from,
                        "transaction_fee": int(gas, 16) * int(gas_price, 16) / 1e18,
                        "gas": int(gas, 16) / 1e9,
                        "gas_price": int(gas_price, 16) / 1e9,
                        "max_fee_per_gas": int(max_fee_per_gas, 16) / 1e9,
                        "max_priority_fee_per_gas": int(max_priority_fee_per_gas, 16) / 1e9,
                        "hash": tx_hash,
                        "input": data,
                        "nonce": int(nonce, 16),
                        "to": address_to,
                        "value": int(value, 16),
                    }
                    pubsub.send(self.topic, tx, silent=self.silent)
