from web3 import Web3


def parse_address_from_topic(topic: str) -> str:
    return Web3.toChecksumAddress("0x" + topic[-40:])
