# -*- coding: utf-8 -*-
import click
from .decorators import online
from .main import main, config
from .ui import print_table, print_tx


@main.group()
def tools():
    """ Further tools
    """
    pass


@tools.command()
@click.pass_context
@online
@click.argument("account")
def getcloudloginkey(ctx, account):
    """ Return keys for cloudlogin
    """
    from meta1base.account import PasswordKey

    password = click.prompt("Passphrase", hide_input=True).strip()
    t = [["role", "wif", "pubkey", "accounts"]]
    for role in ["owner", "active", "memo"]:
        wif = PasswordKey(account, password, role=role)
        pubkey = format(wif.get_public_key(), ctx.meta1.rpc.chain_params["prefix"])

        t.append(
            [
                role,
                str(wif.get_private_key()),
                pubkey,
                ctx.meta1.wallet.getAccountFromPublicKey(pubkey) or "",
            ]
        )

    print_table(t)


@tools.command()
@click.pass_context
@online
@click.option("--limit", default=10, type=int)
def getbrainkeys(ctx, limit):
    """ Return keys for cloudlogin
    """
    from meta1base.account import BrainKey

    password = click.prompt("Passphrase", hide_input=True).strip()
    t = [["index", "wif", "pubkey", "accounts"]]
    wif = BrainKey(password)
    for i in range(limit):
        pubkey = format(wif.get_public_key(), ctx.meta1.rpc.chain_params["prefix"])

        t.append(
            [
                i,
                str(wif.get_private_key()),
                pubkey,
                ctx.meta1.wallet.getAccountFromPublicKey(pubkey) or "",
            ]
        )
        next(wif)

    print_table(t)


@tools.command()
@click.argument("identifiers", nargs=-1)
def operation(identifiers):
    """ Get an operation name/id pair
    """
    from meta1base.operations import operations, getOperationNameForId

    ret = [["id", "name"]]
    for identifier in identifiers:
        try:
            id = int(identifier)
            name = getOperationNameForId(i)
        except Exception:
            name = identifier
            id = operations[name]
        ret.append([id, name])
    print_table(ret)
