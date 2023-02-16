import aiohttp


cookies = {
    "walletAddress": "",
    "authToken": "",
}


async def fetch_bids():
    async with aiohttp.ClientSession(cookies=cookies) as session:
        return await session.get(url="https://core-api.prod.blur.io/v1/collections/otherdeed/executable-bids")
