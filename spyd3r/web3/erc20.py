import asyncio
from loguru import logger


from executor.w3 import w3
from executor.helpers import to_async
from executor.w3.block import block_ws


abi = '[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"spender","type":"address"},{"name":"value","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_owner","type":"address"}],"name":"nominateNewOwner","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"from","type":"address"},{"name":"to","type":"address"},{"name":"value","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"nominatedOwner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_target","type":"address"}],"name":"setTarget","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"acceptOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"callData","type":"bytes"},{"name":"numTopics","type":"uint256"},{"name":"topic1","type":"bytes32"},{"name":"topic2","type":"bytes32"},{"name":"topic3","type":"bytes32"},{"name":"topic4","type":"bytes32"}],"name":"_emit","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"useDELEGATECALL","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"to","type":"address"},{"name":"value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"value","type":"bool"}],"name":"setUseDELEGATECALL","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"target","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"owner","type":"address"},{"name":"spender","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[{"name":"_owner","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"newTarget","type":"address"}],"name":"TargetUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"newOwner","type":"address"}],"name":"OwnerNominated","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"oldOwner","type":"address"},{"indexed":false,"name":"newOwner","type":"address"}],"name":"OwnerChanged","type":"event"}]'


@to_async
def fetch_balance(account_address: str, token_address: str):
    """
    Fetch the balance of a given account for a given address
    """
    contract = w3.eth.contract(
        address=token_address,
        abi=abi,
    )  # type: ignore
    balance = contract.functions.balanceOf(account_address).call()

    return balance / 1e18


class Balance_WS:
    def __init__(self, account_address: str, token_address: str, token_symbol: str):
        # Parameters
        self.account_address = account_address
        self.token_address = token_address
        self.token_symbol = token_symbol

        # Internal variables
        self.started = False
        self.event = asyncio.Event()

    async def start_async(self):
        """
        Start the websocket in an asynchronous manner
        """
        # Initialising the price variables
        self.balance = None

        while True:
            # Waiting for a new block
            await block_ws.event.wait()

            # Fetching prices from one_inch
            balance_new = await fetch_balance(
                account_address=self.account_address,
                token_address=self.token_address,
            )

            if self.balance != balance_new:
                # Signalling a new balance
                self.event.set()
                self.event.clear()

                # Adjusting the price variables
                self.balance = balance_new
                logger.info(f"Balance: {self.balance} {self.token_symbol}")

    async def start_async_safe(self):
        """
        Start the websocket in an asynchronous manner under superivision
        """
        while True:
            try:
                await self.start_async()
            except Exception as e:
                logger.error(e)

    def start(self):
        block_ws.start()
        if not self.started:
            asyncio.ensure_future(self.start_async_safe())
        self.started = True
