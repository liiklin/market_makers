import click
from uptick.decorators import unlock, online
from uptick.main import main
from bitshares.market import Market
import json

@main.command()
@click.argument("source")
@click.argument("allowed")
@click.option("--amount", default=100)
@click.pass_context
@online
def spread(ctx,source, allowed, amount):
    click.echo("%s-%s:%s" % (source, allowed, amount))
    allowed_items = allowed.split(",")
    for item in allowed_items:
        pair = "%s-%s" % (source, item)
        market = Market(pair, bitshares_instance=ctx.bitshares)
        orderbook = market.orderbook()
        click.echo(() % (str(orderbook)))

if __name__ == "__main__":
    main()