import json
from web3.logs import DISCARD

from env import ETH_ADDRESS, ETH_PRIVATE_KEY

from spyd3r.web3 import web3, nonce
from spyd3r.helpers import to_async

abi = json.loads(
    '[{"inputs":[{"internalType":"address","name":"_resolver","type":"address"},{"internalType":"bytes32","name":"_baseAsset","type":"bytes32"},{"internalType":"bytes32","name":"_marketKey","type":"bytes32"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes32","name":"name","type":"bytes32"},{"indexed":false,"internalType":"address","name":"destination","type":"address"}],"name":"CacheUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"int256","name":"funding","type":"int256"},{"indexed":false,"internalType":"uint256","name":"index","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"timestamp","type":"uint256"}],"name":"FundingRecomputed","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"trackingCode","type":"bytes32"},{"indexed":false,"internalType":"bytes32","name":"baseAsset","type":"bytes32"},{"indexed":false,"internalType":"bytes32","name":"marketKey","type":"bytes32"},{"indexed":false,"internalType":"int256","name":"sizeDelta","type":"int256"},{"indexed":false,"internalType":"uint256","name":"fee","type":"uint256"}],"name":"FuturesTracking","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":false,"internalType":"int256","name":"marginDelta","type":"int256"}],"name":"MarginTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":false,"internalType":"uint256","name":"currentRoundId","type":"uint256"},{"indexed":false,"internalType":"int256","name":"sizeDelta","type":"int256"},{"indexed":false,"internalType":"uint256","name":"targetRoundId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"commitDeposit","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"keeperDeposit","type":"uint256"},{"indexed":false,"internalType":"bytes32","name":"trackingCode","type":"bytes32"}],"name":"NextPriceOrderRemoved","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":false,"internalType":"int256","name":"sizeDelta","type":"int256"},{"indexed":false,"internalType":"uint256","name":"targetRoundId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"commitDeposit","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"keeperDeposit","type":"uint256"},{"indexed":false,"internalType":"bytes32","name":"trackingCode","type":"bytes32"}],"name":"NextPriceOrderSubmitted","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"id","type":"uint256"},{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":true,"internalType":"address","name":"liquidator","type":"address"},{"indexed":false,"internalType":"int256","name":"size","type":"int256"},{"indexed":false,"internalType":"uint256","name":"price","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"fee","type":"uint256"}],"name":"PositionLiquidated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"id","type":"uint256"},{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":false,"internalType":"uint256","name":"margin","type":"uint256"},{"indexed":false,"internalType":"int256","name":"size","type":"int256"},{"indexed":false,"internalType":"int256","name":"tradeSize","type":"int256"},{"indexed":false,"internalType":"uint256","name":"lastPrice","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"fundingIndex","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"fee","type":"uint256"}],"name":"PositionModified","type":"event"},{"constant":true,"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"accessibleMargin","outputs":[{"internalType":"uint256","name":"marginAccessible","type":"uint256"},{"internalType":"bool","name":"invalid","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"accruedFunding","outputs":[{"internalType":"int256","name":"funding","type":"int256"},{"internalType":"bool","name":"invalid","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"assetPrice","outputs":[{"internalType":"uint256","name":"price","type":"uint256"},{"internalType":"bool","name":"invalid","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"baseAsset","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"canLiquidate","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"cancelNextPriceOrder","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"closePosition","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"bytes32","name":"trackingCode","type":"bytes32"}],"name":"closePositionWithTracking","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"currentFundingRate","outputs":[{"internalType":"int256","name":"","type":"int256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"executeNextPriceOrder","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"fundingLastRecomputed","outputs":[{"internalType":"uint32","name":"","type":"uint32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"fundingSequence","outputs":[{"internalType":"int128","name":"","type":"int128"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"fundingSequenceLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"isResolverCached","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"liquidatePosition","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"liquidationFee","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"liquidationPrice","outputs":[{"internalType":"uint256","name":"price","type":"uint256"},{"internalType":"bool","name":"invalid","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"marketDebt","outputs":[{"internalType":"uint256","name":"debt","type":"uint256"},{"internalType":"bool","name":"invalid","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"marketKey","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"marketSize","outputs":[{"internalType":"uint128","name":"","type":"uint128"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"marketSizes","outputs":[{"internalType":"uint256","name":"long","type":"uint256"},{"internalType":"uint256","name":"short","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"marketSkew","outputs":[{"internalType":"int128","name":"","type":"int128"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"int256","name":"sizeDelta","type":"int256"}],"name":"modifyPosition","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"int256","name":"sizeDelta","type":"int256"},{"internalType":"bytes32","name":"trackingCode","type":"bytes32"}],"name":"modifyPositionWithTracking","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"nextPriceOrders","outputs":[{"internalType":"int128","name":"sizeDelta","type":"int128"},{"internalType":"uint128","name":"targetRoundId","type":"uint128"},{"internalType":"uint128","name":"commitDeposit","type":"uint128"},{"internalType":"uint128","name":"keeperDeposit","type":"uint128"},{"internalType":"bytes32","name":"trackingCode","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"notionalValue","outputs":[{"internalType":"int256","name":"value","type":"int256"},{"internalType":"bool","name":"invalid","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"int256","name":"sizeDelta","type":"int256"}],"name":"orderFee","outputs":[{"internalType":"uint256","name":"fee","type":"uint256"},{"internalType":"bool","name":"invalid","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"positions","outputs":[{"internalType":"uint64","name":"id","type":"uint64"},{"internalType":"uint64","name":"lastFundingIndex","type":"uint64"},{"internalType":"uint128","name":"margin","type":"uint128"},{"internalType":"uint128","name":"lastPrice","type":"uint128"},{"internalType":"int128","name":"size","type":"int128"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"int256","name":"sizeDelta","type":"int256"},{"internalType":"address","name":"sender","type":"address"}],"name":"postTradeDetails","outputs":[{"internalType":"uint256","name":"margin","type":"uint256"},{"internalType":"int256","name":"size","type":"int256"},{"internalType":"uint256","name":"price","type":"uint256"},{"internalType":"uint256","name":"liqPrice","type":"uint256"},{"internalType":"uint256","name":"fee","type":"uint256"},{"internalType":"enum IFuturesMarketBaseTypes.Status","name":"status","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"profitLoss","outputs":[{"internalType":"int256","name":"pnl","type":"int256"},{"internalType":"bool","name":"invalid","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"rebuildCache","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"recomputeFunding","outputs":[{"internalType":"uint256","name":"lastIndex","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"remainingMargin","outputs":[{"internalType":"uint256","name":"marginRemaining","type":"uint256"},{"internalType":"bool","name":"invalid","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"resolver","outputs":[{"internalType":"contract AddressResolver","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"resolverAddressesRequired","outputs":[{"internalType":"bytes32[]","name":"addresses","type":"bytes32[]"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"int256","name":"sizeDelta","type":"int256"}],"name":"submitNextPriceOrder","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"int256","name":"sizeDelta","type":"int256"},{"internalType":"bytes32","name":"trackingCode","type":"bytes32"}],"name":"submitNextPriceOrderWithTracking","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"int256","name":"marginDelta","type":"int256"}],"name":"transferMargin","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"unrecordedFunding","outputs":[{"internalType":"int256","name":"funding","type":"int256"},{"internalType":"bool","name":"invalid","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"withdrawAllMargin","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]'
)

# Default contract (ETH market)
contract = web3.eth.contract(
    address="0xf86048DFf23cF130107dfB4e6386f574231a5C65",
    abi=abi,
)  # type: ignore


def create_contract(address: str):
    return web3.eth.contract(
        address=address,
        abi=abi,
    )  # type: ignore


@to_async
def fetch_order_fee(size: float, contract=contract):
    """
    Fetch the fees to create an order on a given market
    """
    fees = contract.functions.orderFee(int(size * 1e18)).call()[0]
    return float(web3.from_wei(fees, unit="ether"))


@to_async
def fetch_position(contract=contract):
    """
    Fetch the position on a given market
    """
    position = contract.functions.positions(ETH_ADDRESS).call()[4]
    return float(position / 1e18)


@to_async
def create_order(size: float, contract=contract):
    """
    Create a market order of a given size on the given market
    """
    # Determining the sign of the the size
    if size < 0:
        sign = -1
    else:
        sign = 1

    # Constructing the payload
    payload = {
        "nonce": nonce.fetch(),
        "from": ETH_ADDRESS,
        "to": contract.address,
        "gas": 1000000,  # TODO: to optimise
        "gasPrice": 1000000,  # TODO: to optimise
        "data": contract.encodeABI(fn_name="modifyPosition", args=[sign * web3.to_wei(abs(size), unit="ether")]),
    }

    # Signing the transaction
    signed_tx = web3.eth.account.sign_transaction(payload, private_key=ETH_PRIVATE_KEY)

    # Sending the transaction
    return web3.eth.send_raw_transaction(signed_tx.rawTransaction)


@to_async
def fetch_order(tx_hash):
    receipt = web3.eth.get_transaction_receipt(tx_hash)
    logs = contract.events.PositionModified().processReceipt(receipt, errors=DISCARD)

    if len(logs) > 0:
        #
        order = logs[-1]["args"]

        # Side
        if order["tradeSize"] > 0:
            side = "buy"
        else:
            side = "sell"

        return {
            "side": side,
            "size": abs(order["tradeSize"]) / 1e18,
            "price": order["lastPrice"] / 1e18,
            "fees": order["fee"] / 1e18,
        }
    else:
        return None


@to_async
def fetch_margin(account_address: str, contract=contract):
    """
    Fetch the margin of the given account
    """
    # Fetching the margin
    margin = contract.functions.remainingMargin(account_address).call()[0]

    return margin / 1e18
