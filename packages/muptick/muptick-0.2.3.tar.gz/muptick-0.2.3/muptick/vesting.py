# -*- coding: utf-8 -*-
import click
from prettytable import PrettyTable
from meta1.amount import Amount
from meta1.account import Account
from meta1.price import Price, Order
from meta1.vesting import Vesting
from .decorators import onlineChain, unlockWallet, online, unlock
from .main import main
from .ui import print_tx, print_table


@main.command()
@click.argument("account")
@click.pass_context
@online
def vesting(ctx, account):
    """ List accounts vesting balances
    """
    account = Account(account, full=True)
    t = [["vesting_id", "claimable", "balance_type"]]
    for vest in account["vesting_balances"]:
        vesting = Vesting(vest)
        t.append([vesting["id"], str(vesting.claimable), vesting["balance_type"]])
    print_table(t)


@main.command()
@click.option("--account", default=None)
@click.argument("vestingid")
@click.argument("amount", default=0)
@click.pass_context
@online
@unlock
def claim(ctx, vestingid, account, amount):
    """ Claim funds from the vesting balance
    """
    vesting = Vesting(vestingid)
    if amount:
        amount = Amount(float(amount), "META1")
    else:
        amount = vesting.claimable
    print_tx(
        ctx.meta1.vesting_balance_withdraw(
            vesting["id"], amount=amount, account=vesting["owner"]
        )
    )


@main.command()
@click.option("--account", default=None)
@click.argument("amount", type=float)
@click.argument("symbol", type=str)
@click.pass_context
@online
@unlock
def reserve(ctx, amount, symbol, account):
    """ Reserve/Burn tokens
    """
    print_tx(
        ctx.meta1.reserve(
            Amount(amount, symbol, meta1_instance=ctx.meta1), account=account
        )
    )
