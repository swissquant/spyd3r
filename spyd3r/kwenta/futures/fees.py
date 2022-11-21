import asyncio
from loguru import logger

from .markets import Kwenta_Futures_Markets
from .contracts.future import fetch_order_fee

from link import pubsub, synchroniser, Listener

from spyd3r.oracles.chainlink import Oracle
from spyd3r.helpers import restart_on_failure


class Kwenta_Futures_Fees:

    markets = Kwenta_Futures_Markets()
    topic = "kwenta_futures:trading_fees"

    async def update_fees(self, market: str):
        # Waiting a bit to avoid value jittering
        await asyncio.sleep(3)

        # Calculating the fees (in %)
        fees_long, fees_short = await asyncio.gather(
            fetch_order_fee(size=1, contract=self.markets.contracts[market]),
            fetch_order_fee(size=-1, contract=self.markets.contracts[market]),
        )

        # Broadcasting
        message = {
            "market": market,
            "fees_long": fees_long,
            "fees_short": fees_short,
        }
        pubsub.send(topic=self.topic, message=message)

    @restart_on_failure
    async def start(self):
        listener = Listener(topics=[Oracle.topic_pubsub])
        synchroniser.set("kwenta_futures_fees")

        while True:
            match await listener.pop_msg():
                case {"oracle": market, "answer": _}:
                    if market in self.markets.market_to_address.keys():
                        await self.update_fees(market=market)
                case payload:
                    logger.debug(payload)
