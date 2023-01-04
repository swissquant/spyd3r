import asyncio
import threading
from loguru import logger

from .client import web3

from spyd3r.helpers import to_async, restart_on_failure

from env import ETH_ADDRESS


nonce_lock = threading.Lock()  # Protect against multiple nonce acquisitions


@to_async
def fetch_nonce(address: str) -> float:
    return web3.eth.get_transaction_count(address)


# Nonce manager
class Nonce:
    def __init__(self):
        self.nonce = None

    def fetch(self):
        with nonce_lock:
            self.nonce += 1

            return self.nonce - 1

    @restart_on_failure
    async def start(self, freq_update: float = 60):
        while True:
            with nonce_lock:
                tx_count = await fetch_nonce(address=ETH_ADDRESS)
                self.nonce = max(self.nonce, tx_count)
                logger.info(f"nonce: {self.nonce}")

            await asyncio.sleep(freq_update)


nonce = Nonce()
