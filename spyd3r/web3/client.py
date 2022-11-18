from web3 import Web3

from env import WEB3_NODE


# Web3 client
web3 = Web3(Web3.HTTPProvider(WEB3_NODE))
