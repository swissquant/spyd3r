import json
import asyncio
import aiohttp
import websockets
from loguru import logger

from .client import web3

from env import WEB3_NODE, ETH_PRIVATE_KEY


class TX_WS:
    def __init__(self, address: str):
        # Class variables
        self.address = address

        # Internal variables
        self.started = False
        self.event = asyncio.Event()

    async def connect(self):
        """
        Connect to the websocket endpoint
        """
        url = WEB3_NODE.replace("https", "wss")
        self.ws = await websockets.connect(url)

    async def subscribe(self):
        """
        Subscribe to the desired feed
        """
        payload = {
            "id": 1,
            "method": "eth_subscribe",
            "params": [
                "logs",
                {
                    "address": self.address,
                },
            ],
        }
        await self.ws.send(json.dumps(payload))

    async def start_async(self):
        """
        Start the websocket in an asynchronous manner
        """
        # Setting up the WS
        await self.connect()
        await self.subscribe()

        # Logging a lil' so those biatchs know what's up in the hood
        logger.info("WS is on!")

        while True:
            # Waiting for a new tx
            await self.ws.recv()

            # Signalling the new block
            self.event.set()
            self.event.clear()
            logger.info("New TX")

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
        if not self.started:
            asyncio.ensure_future(self.start_async_safe())
        self.started = True


async def fetch_transactions(address: str):
    """
    Fetch all the transactions for a given address
    """
    url = f"https://api-optimistic.etherscan.io/api?module=account&action=txlist&address={address}&sort=desc"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            transactions = await resp.json()

    return transactions["result"]


async def submit_transaction(payload):
    # Sign the transaction
    tx = web3.eth.account.sign_transaction(payload, private_key=ETH_PRIVATE_KEY)

    # Submit the transaction
    loop = asyncio.get_running_loop()
    hash = await loop.run_in_executor(None, web3.eth.send_raw_transaction, tx.rawTransaction)

    return hash


async def wait_for_receipt(hash):
    loop = asyncio.get_running_loop()
    receipt = await loop.run_in_executor(None, web3.eth.wait_for_transaction_receipt, hash.hex())

    return receipt


def is_success(receipt: dict):
    return receipt.get("status", 0) == 1
