import math
import click
from prettytable import PrettyTable
from pprint import pprint
from tqdm import tqdm
from meta1.market import Market
from meta1.price import Price
from meta1.witness import Witness, Witnesses
from meta1.asset import Asset
from datetime import datetime, timedelta
from .decorators import onlineChain, unlockWallet
from .main import main, config
from .ui import print_tx


@main.command()
@click.pass_context
@onlineChain
@click.argument("symbol", type=str, nargs=1)
@click.argument("price", type=float, nargs=1)
@click.argument("market", type=str, nargs=1)
@click.option(
    "--account",
    help="Account that takes this action",
    default=config["default_account"],
    type=str,
)
@click.option("--cer", help="Core Exchange Rate", default=None, type=float)
@click.option(
    "--mssr",
    help="Percentage for max short squeeze ratio (e.g., 110)",
    default=110,
    type=float,
)
@click.option(
    "--mcr",
    help="Percentage for maintenance collateral ratio (e.g., 200)",
    default=200,
    type=float,
)
@unlockWallet
def newfeed(ctx, symbol, price, market, cer, mssr, mcr, account):
    """ Publish a price feed!

        Examples:

            \b
            muptick newfeed USD 0.01 USD/META1
            muptick newfeed USD 100 META1/USD

        Core Exchange Rate (CER)
        \b
        If no CER is provided, the cer will be the same as the settlement price
        with a 5% premium (Only if the 'market' is against the core asset (e.g.
        META1)). The CER is always defined against the core asset (META1). This
        means that if the backing asset is not the core asset (META1), then you must
        specify your own cer as a float. The float `x` will be interpreted as
        `x META1/SYMBOL`.
    """
    if cer:
        cer = Price(cer, quote=symbol, base="1.3.0", meta1_instance=ctx.meta1)

    print_tx(
        ctx.meta1.publish_price_feed(
            symbol, Price(price, market), cer=cer, mssr=mssr, mcr=mcr, account=account
        )
    )


@main.command()
@click.pass_context
@onlineChain
@click.argument("assets", nargs=-1)
@click.option(
    "--pricethreshold", help="Percentage threshold for price", default=5.0, type=float
)
@click.option("--maxage", help="Max Age in minutes", default=60.0 * 24, type=float)
def feeds(ctx, assets, pricethreshold, maxage):
    """ Price Feed Overview
    """
    import builtins

    witnesses = Witnesses(meta1_instance=ctx.meta1)

    def test_price(p, ref):
        if math.fabs(float(p / ref) - 1.0) > pricethreshold / 100.0:
            return click.style(str(p), fg="red")
        elif math.fabs(float(p / ref) - 1.0) > pricethreshold / 2.0 / 100.0:
            return click.style(str(p), fg="yellow")
        else:
            return click.style(str(p), fg="green")

    def price_diff(p, ref):
        d = (float(p) - float(ref)) / float(ref) * 100
        if math.fabs(d) >= 5:
            color = "red"
        elif math.fabs(d) >= 2.5:
            color = "yellow"
        else:
            color = "green"
        return click.style("{:8.2f}%".format(d), fg=color)

    def test_date(d):
        t = d.replace(tzinfo=None)
        now = datetime.utcnow()
        if now < t + timedelta(minutes=maxage):
            return click.style(str(t), fg="green")
        if now < t + timedelta(minutes=maxage / 2.0):
            return click.style(str(t), fg="yellow")
        else:
            return click.style(str(t), fg="red")

    output = ""
    for asset in tqdm(assets):
        t = PrettyTable(
            [
                "Asset",
                "Producer",
                "Active Witness",
                "Date",
                "Settlement Price",
                "Core Exchange Price",
                "MCR",
                "SSPR",
                "delta",
            ]
        )
        t.align = "c"
        t.align["Producer"] = "l"
        asset = Asset(asset, full=True, meta1_instance=ctx.meta1)
        current_feed = asset.feed
        feeds = asset.feeds
        producingwitnesses = builtins.set()
        witness_accounts = [x["witness_account"] for x in witnesses]
        for feed in tqdm(feeds):
            producingwitnesses.add(feed["producer"]["id"])
            t.add_row(
                [
                    asset["symbol"],
                    feed["producer"]["name"],
                    click.style(
                        "X" if feed["producer"]["id"] in witness_accounts else "",
                        bold=True,
                    ),
                    test_date(feed["date"]),
                    test_price(
                        feed["settlement_price"], current_feed["settlement_price"]
                    ),
                    test_price(
                        feed["core_exchange_rate"], current_feed["core_exchange_rate"]
                    ),
                    feed["maintenance_collateral_ratio"] / 10,
                    feed["maximum_short_squeeze_ratio"] / 10,
                    price_diff(
                        feed["core_exchange_rate"], current_feed["core_exchange_rate"]
                    ),
                ]
            )
        for missing in builtins.set(witness_accounts).difference(producingwitnesses):
            witness = Witness(missing)
            t.add_row(
                [
                    click.style(asset["symbol"], bg="red"),
                    click.style(witness.account["name"], bg="red"),
                    click.style(
                        "X" if feed["producer"]["id"] in witness_accounts else "",
                        bold=True,
                    ),
                    click.style(str(datetime(1970, 1, 1))),
                    click.style("missing", bg="red"),
                    click.style("missing", bg="red"),
                    click.style("missing", bg="red"),
                    click.style("missing", bg="red"),
                    click.style("missing", bg="red"),
                ]
            )
        output += t.get_string(sortby="Date", reversesort=True)
        output += "\n"
    click.echo(output)
