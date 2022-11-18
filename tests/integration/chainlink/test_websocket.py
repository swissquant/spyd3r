import asyncio

from spyd3r.oracles.chainlink import Oracle, oracles_optimism


asyncio.run(Oracle(oracles_optimism).start())
