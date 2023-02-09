import asyncio

from spyd3r.blur import Sales

from env import WEB3_NODE


asyncio.run(Sales(rpc_endpoint=WEB3_NODE).start())
