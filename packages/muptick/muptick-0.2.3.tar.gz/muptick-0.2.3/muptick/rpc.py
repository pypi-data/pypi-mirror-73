import click
from pprint import pprint
from .decorators import onlineChain
from .main import main
from .ui import print_dict


@main.command()
@click.pass_context
@onlineChain
@click.argument("call", nargs=1)
@click.argument("arguments", nargs=-1)
@click.option(
    "--api", default="database", help="Provide API node, if not 'database'", type=str
)
def rpc(ctx, call, arguments, api):
    """ Construct RPC call directly
        \b
        You can specify which API to send the call to:

            muptick rpc --api assets

        You can also specify lists using

            muptick rpc get_objects "['2.0.0', '2.1.0']"

    """
    try:
        data = list(eval(d) for d in arguments)
    except:
        data = arguments
    ret = getattr(ctx.meta1.rpc, call)(*data, api=api)
    print_dict(ret)
