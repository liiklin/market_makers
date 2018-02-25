import click
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil as tsu
import pandas as pd
import numpy as np
from math import sqrt

from simulate import process_orders, get_close_prices

def similate_portfolio(initial_amount, df_orders, custom_enddate=None):
    """
    Load the orders_file as csv.
    Convert it and the initia_amount to dict_orders.
    Call simulate with the dict.
    Write the results to out-file.
    """
    df_orders.columns = ["year","month","day","symbol","bs","amount","xx"]
    for c in ["symbol","bs"]:
        df_orders[c] = df_orders[c].map(str.strip)

    df_orders["amount"] = np.where(df_orders["bs"].str.upper() =="SELL", (df_orders["amount"] * -1), df_orders["amount"])
    ts_dates = pd.to_datetime((df_orders.year*10000+df_orders.month*100+df_orders.day).apply(str),format='%Y%m%d')
    df = df_orders[["symbol","amount"]]
    df = df.pivot(columns='symbol', values='amount')
    df["date"]=ts_dates
   
    df_result = process_orders(df, float(initial_amount))
    return df_result

@click.command()
@click.argument("initial_amount")
@click.argument("orders_file", type=click.Path(exists=True))
@click.argument("out_file")
def main(initial_amount, orders_file, out_file):
    df_orders = pd.read_csv(orders_file, header=None)
    df_portfolio = similate_portfolio(initial_amount, df_orders)
    start_date = df_portfolio.index[0]
    end_date = df_portfolio.index[-1]
    
    df_portfolio[["year","month","day","portfolio"]].to_csv(out_file,header=False,index=False)
    spx_prices = get_close_prices(start_date, end_date, ["$SPX"])["$SPX"].values
    spx_ret = tsu.returnize0(spx_prices.copy())
    p_ret = tsu.returnize0(df_portfolio["portfolio"].values.copy())
    print "Details of the Performance of the portfolio :"
    print "Data Range :  %s  to  %s\n" % (start_date, end_date)
    print "Sharpe Ratio of Fund : %s" % ((sqrt(252) * p_ret.mean()/p_ret.std()))
    print "Sharpe Ratio of $SPX : %s\n" %((sqrt(252) * spx_ret.mean()/spx_ret.std()))
    print "Total Return of Fund :  %s" % (df_portfolio["portfolio"][-1]/df_portfolio["portfolio"][0])
    print "Total Return of $SPX : %s\n" %(spx_prices[-1]/spx_prices[0])
    print "Standard Deviation of Fund :  %s" % (p_ret.std())
    print "Standard Deviation of $SPX : %s\n" % (spx_ret.std())
    print"Average Daily Return of Fund :  %s" % (p_ret.mean())
    print "Average Daily Return of $SPX : %s" % (spx_ret.mean())

if "__main__" in __name__:
    main()