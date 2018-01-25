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
        orders_ask = parse_orders(orderbook["asks"],"ask")
        for order in orders_ask:
            click.echo("base symbol %s" % (order["base"]["asset"]["symbol"]))
            click.echo("base %s" % (order["base"]))
            click.echo("price %s" %(order["price"]))
            click.echo("quote symbol %s" % (order["quote"]["asset"]["symbol"]))
            click.echo("buy %s %s @ %s %s/%s for %s %s" % \
                (order["quote"]["amount"], order["quote"]["asset"]["symbol"],
                order["price"], order["base"]["asset"]["symbol"], order["quote"]["asset"]["symbol"], 
                order["base"]["amount"], order["base"]["asset"]["symbol"]))
            click.echo("order: %s" %(order.json()))
def parse_orders(items, type):
    orders = []
    for item in items:
        #s_item = item.split(" ")
        #orders.append({"type":type, "amount_from":float(s_item[0]), "from_asset":s_item[1], 
        #"amount_to":float(s_item[2]), "to_assert":s_item[3], 
        #"price":float(s_item[5]), "currency_pair":s_item[6]})
        orders.append(item)
    return orders

if __name__ == "__main__":
    main()