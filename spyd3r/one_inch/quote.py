import urllib
import aiohttp

from .map import coin_to_address, chain_to_code


async def fetch_quote(chain: str, coin_in: str, coin_out: str, amount: float, precision=1e18):
    code = chain_to_code[chain]
    url = f"https://api.1inch.exchange/v3.0/{code}/quote"
    p = {
        "fromTokenAddress": coin_to_address[chain][coin_in],
        "toTokenAddress": coin_to_address[chain][coin_out],
        "amount": int(amount * precision),
    }
    url += f"?{urllib.parse.urlencode(p)}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            quote = await response.json()

    if quote.get("description") == "insufficient liquidity":
        return 0.0

    return float(quote["toTokenAmount"]) / float(quote["fromTokenAmount"])
