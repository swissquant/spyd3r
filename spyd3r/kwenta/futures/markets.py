from .contracts.future import create_contract, create_order


class Kwenta_Futures_Markets:
    market_to_address = {
        "BTC/USD": "0xEe8804d8Ad10b0C3aD1Bd57AC3737242aD24bB95",
        "ETH/USD": "0xf86048DFf23cF130107dfB4e6386f574231a5C65",
        "SOL/USD": "0xcF853f7f8F78B2B801095b66F8ba9c5f04dB1640",
        "AVAX/USD": "0x4ff54624D5FB61C34c634c3314Ed3BfE4dBB665a",
        "LINK/USD": "0x1228c7D8BBc5bC53DB181bD7B1fcE765aa83bF8A",
        "MATIC/USD": "0xbCB2D435045E16B059b2130b28BE70b5cA47bFE5",
        "AAVE/USD": "0x001b7876F567f0b3A639332Ed1e363839c6d85e2",
        "UNI/USD": "0x5Af0072617F7f2AEB0e314e2faD1DE0231Ba97cD",
        "APE/USD": "0xFe00395ec846240dc693e92AB2Dd720F94765Aa3",
        "DYDX/USD": "0x10305C1854d6DB8A1060dF60bDF8A8B2981249Cf",
        "DOGE/USD": "0x9f231dBE53D460f359B2B8CC47574493caA5B7Bf",
        "BNB/USD": "0x4Aa0dabd22BC0894975324Bec293443c8538bD08",
        "OP/USD": "0x9F1C2f0071Bc3b31447AEda9fA3A68d651eB4632",
        "XMR/USD": "0x3Ed04CEfF4c91872F19b1da35740C0Be9CA21558",
    }

    def __init__(self) -> None:
        # Mapping tables
        self.address_to_market = dict((v, k) for k, v in self.market_to_address.items())

        # Creating the contracts
        self.contracts = {}
        for market, address_contract in self.market_to_address.items():
            self.contracts[market] = create_contract(address=address_contract)

    async def post_market_order(self, market: str, size: float):
        return await create_order(size=size, contract=self.contracts[market])
