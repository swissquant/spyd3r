import asyncio

from spyd3r.web3.nonce import fetch_nonce
from env import ETH_ADDRESS


print(asyncio.run(fetch_nonce(address=ETH_ADDRESS)))
