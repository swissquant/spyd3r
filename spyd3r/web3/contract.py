from web3 import Web3


class Contract:
    abi = ""

    def __init__(self, rpc_endpoint: str, address: str):
        self.web3 = Web3(Web3.HTTPProvider(rpc_endpoint))
        self.contract = self.web3.eth.contract(address=address, abi=self.abi)  # type: ignore

    def set_address(self, address: str):
        self.contract = self.web3.eth.contract(address=address, abi=self.abi)  # type: ignore
