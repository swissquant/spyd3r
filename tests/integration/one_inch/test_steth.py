import asyncio

from spyd3r.one_inch import fetch_quote


quote = asyncio.run(fetch_quote(chain="ethereum", coin_in="steth", coin_out="eth", amount=4000))
print(quote)
