_contract_to_market = {
    "0xf86048DFf23cF130107dfB4e6386f574231a5C65".lower(): "ETH-PERP",
    "0x1228c7D8BBc5bC53DB181bD7B1fcE765aa83bF8A".lower(): "LINK-PERP",
    "0xEe8804d8Ad10b0C3aD1Bd57AC3737242aD24bB95".lower(): "BTC-PERP",
    "0x4ff54624D5FB61C34c634c3314Ed3BfE4dBB665a".lower(): "AVAX-PERP",
    "0xcF853f7f8F78B2B801095b66F8ba9c5f04dB1640".lower(): "SOL-PERP",
    "0x5Af0072617F7f2AEB0e314e2faD1DE0231Ba97cD".lower(): "UNI-PERP",
    "0xbCB2D435045E16B059b2130b28BE70b5cA47bFE5".lower(): "MATIC-PERP",
    "0x001b7876F567f0b3A639332Ed1e363839c6d85e2".lower(): "AAVE-PERP",
    "0xFe00395ec846240dc693e92AB2Dd720F94765Aa3".lower(): "APE-PERP",
    "0x10305C1854d6DB8A1060dF60bDF8A8B2981249Cf".lower(): "DYDX-PERP",
}

_market_to_contract = {v: k for k, v in _contract_to_market.items()}


def contract_to_market(contract: str) -> str:
    return _contract_to_market.get(contract.lower(), contract.lower())


def market_to_contract(market: str) -> str:
    return _market_to_contract.get(market.lower(), market.lower())
