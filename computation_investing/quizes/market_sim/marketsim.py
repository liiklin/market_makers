import click
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.DataAccess as da
from simluate import *
@click.command()
@click.argument("initial_amount")
@click.argument("orders_file", type=click.Path(exists=True))
@click.argument("out_file")
def main(inital_amount, orders_file, out_file):
    """
    Load the orders_file as csv.
    Convert it and the initia_amount to dict_orders.
    Call simulate with the dict.
    Write the results to out-file.
    """
    
if "__main__" in __name__:
    main()