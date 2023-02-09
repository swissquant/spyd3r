from web3 import Web3
from eth_abi import decode_abi

from link import pubsub
from spyd3r.web3 import Logs, parse_address_from_topic


class Sales(Logs):

    pubsub_topic = "blur:sales"

    def __init__(self, rpc_endpoint: str):
        super().__init__(
            rpc_endpoint=rpc_endpoint,
            address="0x000000000000ad05ccc4f10045630fb830b95127",
            topic="0x61cbb2a3dee0b6064c2e681aadd61677fb4ef319f0b547508d495626f5a62f64",
        )

    def process(self, tx_hash: str, topics: list, data):
        # Extracting the address
        buyer = parse_address_from_topic(topic=topics[1])
        seller = parse_address_from_topic(topic=topics[2])

        # Decoding the data
        data = bytes.fromhex(data[2:])
        data = decode_abi(
            [
                "uint256",
                "uint256",
                "uint256",
                "uint256",
                "uint256",
                "uint256",
                "uint256",
                "address",
                "uint256",
                "uint256",
                "uint256",
                "uint256",
            ],
            data,
        )

        # Extracting the collection address and the price
        collection = Web3.toChecksumAddress(data[7])
        price = float(Web3.from_wei(data[11], unit="ether"))

        # Sending a pub/sub message
        message = {"hash": tx_hash, "buyer": buyer, "seller": seller, "collection": collection, "price": price}
        pubsub.send(topic=self.pubsub_topic, message=message)
