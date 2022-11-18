import json
import asyncio
import websockets
from loguru import logger

from env import WEB3_NODE


class Block_WS:
    def __init__(self):
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
        payload = {"id": 1, "method": "eth_subscribe", "params": ["newHeads"]}
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
            # Waiting for a new block
            await self.ws.recv()

            # Signalling the new block
            self.event.set()
            self.event.clear()
            logger.info("New Ethereum block")

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


block_ws = Block_WS()
