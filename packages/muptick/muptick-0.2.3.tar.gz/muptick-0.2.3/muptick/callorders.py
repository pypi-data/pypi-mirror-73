import sys
import click
from prettytable import PrettyTable
from click_datetime import Datetime
from datetime import datetime, timedelta
from meta1.market import Market
from meta1.amount import Amount
from meta1.account import Account
from meta1.price import Price, Order
from .decorators import onlineChain, unlockWallet, online, unlock
from .main import main, config
from .ui import print_table, print_message


@main.command()
@click.pass_context
@onlineChain
@click.argument("obj", required=False, default=config["default_account"], type=str)
@click.option("--limit", type=int, default=10)
def calls(ctx, obj, limit):
    """ List call/short positions of an account or an asset
    """
    if obj.upper() == obj:
        # Asset
        from meta1.asset import Asset

        asset = Asset(obj, full=True)
        calls = asset.get_call_orders(limit)
        t = [["acount", "debt", "collateral", "call price", "ratio"]]
        for call in calls:
            t.append(
                [
                    str(call["account"]["name"]),
                    str(call["debt"]),
                    str(call["collateral"]),
                    str(call["call_price"]),
                    "%.2f" % (call["ratio"]),
                ]
            )
        print_table(t)
    else:
        # Account
        from meta1.dex import Dex

        dex = Dex(meta1_instance=ctx.meta1)
        calls = dex.list_debt_positions(account=obj)
        t = [["debt", "collateral", "call price", "ratio"]]
        for symbol in calls:
            t.append(
                [
                    str(calls[symbol]["debt"]),
                    str(calls[symbol]["collateral"]),
                    str(calls[symbol]["call_price"]),
                    "%.2f" % (calls[symbol]["ratio"]),
                ]
            )
        print_table(t)


@main.command()
@click.pass_context
@onlineChain
@click.argument("asset", type=str)
@click.option("--limit", type=int, default=10)
def settlements(ctx, asset, limit):
    """ Show pending settlement orders of a bitasset
    """
    from meta1.asset import Asset

    asset = Asset(asset, full=True)
    if not asset.is_bitasset:
        print_message("{} is not a bitasset.".format(asset["symbol"]), "warning")
        sys.exit(1)
    calls = asset.get_settle_orders(limit)
    t = [["acount", "amount", "date"]]
    for call in calls:
        t.append([str(call["account"]["name"]), str(call["amount"]), str(call["date"])])
    print_table(t)
