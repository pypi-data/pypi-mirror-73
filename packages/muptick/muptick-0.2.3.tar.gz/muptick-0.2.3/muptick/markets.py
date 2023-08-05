import click
from click_datetime import Datetime
from datetime import datetime, timedelta
from meta1.market import Market
from meta1.amount import Amount
from meta1.account import Account
from meta1.price import Price, Order
from .decorators import onlineChain, unlockWallet, online, unlock
from .ui import print_tx, print_table, format_table
from .main import main, config


@main.command()
@click.pass_context
@onlineChain
@click.argument("market", nargs=1)
@click.option(
    "--limit", type=int, help="Limit number of elements", default=10
)  # fixme add start and stop time
@click.option(
    "--start",
    help="Start datetime '%Y-%m-%d %H:%M:%S'",
    type=Datetime(format="%Y-%m-%d %H:%M:%S"),
)
@click.option(
    "--stop",
    type=Datetime(format="%Y-%m-%d %H:%M:%S"),
    help="Stop datetime '%Y-%m-%d %H:%M:%S'",
    default=datetime.utcnow(),
)
def trades(ctx, market, limit, start, stop):
    """ List trades in a market
    """
    market = Market(market, meta1_instance=ctx.meta1)
    t = [["time", "quote", "base", "price"]]
    for trade in market.trades(limit, start=start, stop=stop):
        t.append(
            [
                str(trade["time"]),
                str(trade["quote"]),
                str(trade["base"]),
                "{:f} {}/{}".format(
                    trade["price"],
                    trade["base"]["asset"]["symbol"],
                    trade["quote"]["asset"]["symbol"],
                ),
            ]
        )
    print_table(t)


@main.command()
@click.pass_context
@onlineChain
@click.argument("market", nargs=1)
def ticker(ctx, market):
    """ Show ticker of a market
    """
    market = Market(market, meta1_instance=ctx.meta1)
    ticker = market.ticker()
    t = [["key", "value"]]
    for key in ticker:
        t.append([key, str(ticker[key])])
    print_table(t)


@main.command()
@click.pass_context
@onlineChain
@click.argument("orders", type=str, nargs=-1)
@click.option(
    "--account",
    default=config["default_account"],
    type=str,
    help="Account to use for this action",
)
@unlockWallet
def cancel(ctx, orders, account):
    """ Cancel one or multiple orders
    """
    print_tx(ctx.meta1.cancel(orders, account=account))


@main.command()
@click.pass_context
@onlineChain
@click.argument("market", nargs=1)
def orderbook(ctx, market):
    """ Show the orderbook of a particular market
    """
    market = Market(market, meta1_instance=ctx.meta1)
    orderbook = market.orderbook()
    ta = {}
    ta["bids"] = [["quote", "sum quote", "base", "sum base", "price"]]
    cumsumquote = Amount(0, market["quote"])
    cumsumbase = Amount(0, market["base"])
    for order in orderbook["bids"]:
        cumsumbase += order["base"]
        cumsumquote += order["quote"]
        ta["bids"].append(
            [
                str(order["quote"]),
                str(cumsumquote),
                str(order["base"]),
                str(cumsumbase),
                "{:f} {}/{}".format(
                    order["price"],
                    order["base"]["asset"]["symbol"],
                    order["quote"]["asset"]["symbol"],
                ),
            ]
        )

    ta["asks"] = [["price", "base", "sum base", "quote", "sum quote"]]
    cumsumquote = Amount(0, market["quote"])
    cumsumbase = Amount(0, market["base"])
    for order in orderbook["asks"]:
        cumsumbase += order["base"]
        cumsumquote += order["quote"]
        ta["asks"].append(
            [
                "{:f} {}/{}".format(
                    order["price"],
                    order["base"]["asset"]["symbol"],
                    order["quote"]["asset"]["symbol"],
                ),
                str(order["base"]),
                str(cumsumbase),
                str(order["quote"]),
                str(cumsumquote),
            ]
        )
    t = [["bids", "asks"]]
    t.append([format_table(ta["bids"]), format_table(ta["asks"])])
    print_table(t)


@main.command()
@click.pass_context
@onlineChain
@click.argument("buy_amount", type=float)
@click.argument("buy_asset", type=str)
@click.argument("price", type=float)
@click.argument("sell_asset", type=str)
@click.option("--order-expiration", default=None)
@click.option(
    "--account",
    default=config["default_account"],
    type=str,
    help="Account to use for this action",
)
@unlockWallet
def buy(ctx, buy_amount, buy_asset, price, sell_asset, order_expiration, account):
    """ Buy a specific asset at a certain rate against a base asset
    """
    amount = Amount(buy_amount, buy_asset)
    price = Price(
        price, base=sell_asset, quote=buy_asset, meta1_instance=ctx.meta1
    )
    print_tx(
        price.market.buy(price, amount, account=account, expiration=order_expiration)
    )


@main.command()
@click.pass_context
@onlineChain
@click.argument("sell_amount", type=float)
@click.argument("sell_asset", type=str)
@click.argument("price", type=float)
@click.argument("buy_asset", type=str)
@click.option("--order-expiration", default=None)
@click.option(
    "--account",
    default=config["default_account"],
    help="Account to use for this action",
    type=str,
)
@unlockWallet
def sell(ctx, sell_amount, sell_asset, price, buy_asset, order_expiration, account):
    """ Sell a specific asset at a certain rate against a base asset
    """
    amount = Amount(sell_amount, sell_asset)
    price = Price(
        price, quote=sell_asset, base=buy_asset, meta1_instance=ctx.meta1
    )
    print_tx(
        price.market.sell(price, amount, account=account, expiration=order_expiration)
    )


@main.command()
@click.pass_context
@onlineChain
@click.argument("account", type=str)
def openorders(ctx, account):
    """ List open orders of an account
    """
    account = Account(
        account or config["default_account"], meta1_instance=ctx.meta1
    )
    t = [["Price", "Quote", "Base", "ID"]]
    for o in account.openorders:
        t.append(
            [
                "{:f} {}/{}".format(
                    o["price"],
                    o["base"]["asset"]["symbol"],
                    o["quote"]["asset"]["symbol"],
                ),
                str(o["quote"]),
                str(o["base"]),
                o["id"],
            ]
        )
    print_table(t)


@main.command()
@click.option("--account", default=None)
@click.argument("market")
@click.pass_context
@online
@unlock
def cancelall(ctx, market, account):
    """ Cancel all orders of an account in a market
    """
    market = Market(market)
    ctx.meta1.bundle = True
    market.cancel([x["id"] for x in market.accountopenorders(account)], account=account)
    print_tx(ctx.meta1.txbuffer.broadcast())


@main.command()
@click.option("--account", default=None)
@click.argument("market")
@click.argument("side", type=click.Choice(["buy", "sell"]))
@click.argument("min", type=float)
@click.argument("max", type=float)
@click.argument("num", type=float)
@click.argument("total", type=float)
@click.option("--order-expiration", default=None)
@click.pass_context
@online
@unlock
def spread(ctx, market, side, min, max, num, total, order_expiration, account):
    """ Place multiple orders

        \b
        :param str market: Market pair quote:base (e.g. USD:META1)
        :param str side: ``buy`` or ``sell`` quote
        :param float min: minimum price to place order at
        :param float max: maximum price to place order at
        :param int num: Number of orders to place
        :param float total: Total amount of quote to use for all orders
        :param int order_expiration: Number of seconds until the order expires from the books

    """
    from tqdm import tqdm
    from numpy import linspace

    market = Market(market)
    ctx.meta1.bundle = True

    if min < max:
        space = linspace(min, max, num)
    else:
        space = linspace(max, min, num)

    func = getattr(market, side)
    for p in tqdm(space):
        func(p, total / float(num), account=account, expiration=order_expiration)
    print_tx(ctx.meta1.txbuffer.broadcast())


@main.command()
@click.pass_context
@onlineChain
@click.argument("amount", type=float)
@click.argument("symbol", type=str)
@click.option("--ratio", default=None, help="Collateral Ratio", type=float)
@click.option(
    "--account",
    default=config["default_account"],
    help="Account to use for this action",
    type=str,
)
@unlockWallet
def borrow(ctx, amount, symbol, ratio, account):
    """ Borrow a bitasset/market-pegged asset
    """
    from meta1.dex import Dex

    dex = Dex(meta1_instance=ctx.meta1)
    print_tx(
        dex.borrow(Amount(amount, symbol), collateral_ratio=ratio, account=account)
    )


@main.command()
@click.pass_context
@onlineChain
@click.argument("symbol", type=str)
@click.option("--ratio", default=2, help="Collateral Ratio", type=float)
@click.option(
    "--account",
    default=config["default_account"],
    help="Account to use for this action",
    type=str,
)
@unlockWallet
def updateratio(ctx, symbol, ratio, account):
    """ Update the collateral ratio of a call positions
    """
    from meta1.dex import Dex

    dex = Dex(meta1_instance=ctx.meta1)
    print_tx(dex.adjust_collateral_ratio(symbol, ratio, account=account))


@main.command()
@click.pass_context
@onlineChain
@click.argument("symbol", type=str)
@click.argument("amount", type=float)
@click.option(
    "--account",
    default=config["default_account"],
    type=str,
    help="Account to use for this action",
)
@unlockWallet
def fundfeepool(ctx, symbol, amount, account):
    """ Fund the fee pool of an asset
    """
    print_tx(ctx.meta1.fund_fee_pool(symbol, amount, account=account))


@main.command()
@click.pass_context
@onlineChain
@click.argument("collateral_amount", type=float)
@click.argument("collateral_symbol", type=str)
@click.argument("debt_amount", type=float)
@click.argument("debt_symbol", type=str)
@click.option(
    "--account",
    default=config["default_account"],
    type=str,
    help="Account to use for this action",
)
@unlockWallet
def bidcollateral(
    ctx, collateral_symbol, collateral_amount, debt_symbol, debt_amount, account
):
    """ Bid for collateral in the settlement fund
    """
    print_tx(
        ctx.meta1.bid_collateral(
            Amount(collateral_amount, collateral_symbol),
            Amount(debt_amount, debt_symbol),
            account=account,
        )
    )


@main.command()
@click.pass_context
@onlineChain
@click.argument("amount", type=float)
@click.argument("symbol", type=str)
@click.option(
    "--account",
    default=config["default_account"],
    type=str,
    help="Account to use for this action",
)
@unlockWallet
def settle(ctx, symbol, amount, account):
    """ Fund the fee pool of an asset
    """
    print_tx(ctx.meta1.asset_settle(Amount(amount, symbol), account=account))
