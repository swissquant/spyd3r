import asyncio

from spyd3r.lido import fetch_total_supply


print(asyncio.run(fetch_total_supply()))
