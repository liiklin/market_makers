import fileinput
import click
import numpy as np

from datetime import datetime
from datetime import timedelta
from operator import itemgetter
import pandas as pd
import datetime as dt
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.DataAccess as da
import dateutil.parser

def ignore_exception(IgnoreException=Exception,DefaultVal=None):
    """ Decorator for ignoring exception from a function
    e.g.   @ignore_exception(DivideByZero)
    e.g.2. ignore_exception(DivideByZero)(Divide)(2/0)
    """
    def dec(function):
        def _dec(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except IgnoreException:
                return DefaultVal
        return _dec
    return dec

    
def get_next_open_price(prices, date, symbol):
    open_prices = prices["open"]
    any_matches = lambda : open_prices[open_prices.index >date].shape[0] > 0
    if any_matches():
        return float(open_prices[open_prices.index >date].iloc[0][symbol])
    
    return None

def process_orders(orders, initial_cash=10000):
    add_16h = lambda dt: dt + timedelta(hours=16) 
    #orders  = sorted(orders, key=itemgetter("date"))
    orders["date"] = map(add_16h, orders["date"])
    df_orders=pd.DataFrame(orders)
    df_orders = df_orders.set_index("date")
    #ls_symbols = list(set([x["symbol"] for x in orders if not "PORTFOLIO" in x["symbol"]]))
    ls_symbols = list(df_orders.columns.values)
    #ls_symbols = np.loadtxt("/mnt/extradrive1/projects/market_makers/computation_investing/quizes/event_study/short.txt",dtype='S10',comments='#')
    dt_start = df_orders.index[0] + dt.timedelta(days=-1)
    dt_end = df_orders.index[-1]
    #dt_start = min([x["date"] for x in orders]) - timedelta(days=1)
    #dt_end = max([x["date"] for x in orders]) + timedelta(days=1)
    #dt_start = dt.datetime(int(2008) - 1,1,1)
    #dt_end = dt.datetime(int(2008),12,31)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))
    dataobj = da.DataAccess("Yahoo", verbose=True)
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys, verbose=True)
    for d in ldf_data:
        d.fillna(method="pad")
        d.fillna(method="bfill")
    d_data = dict(zip(ls_keys, ldf_data))
    df_prices_close = d_data["close"]
    df_zeros = pd.DataFrame(0,ldt_timestamps, columns=ls_symbols)
    # drop any orders not on trading days
    df_order_wrong_day = df_orders[~df_orders.index.isin(df_zeros.index)]
    print ("Dropping Orders on Market Closed Days...")
    print (df_order_wrong_day)
    df_orders.drop(df_order_wrong_day.index, inplace=True)
    # create a data frame with rows for each date in range
    # containing the trade values
    df_order_trades = df_orders.combine_first(df_zeros)
    # Calculate the cash value of each trade using close prices
    df_trade_values = df_order_trades * df_prices_close
    # Calculate the porfolio stock holdings for each day
    df_portfolio_holdings = df_order_trades.cumsum(axis=0)
    # Calculate the cash portion of the portfolio
    df_portfolio_cash = ((df_trade_values.sum(axis=1) * -1) + initial_cash).cumsum()
    # Calcuate the cash value of the portfolio stock holdings
    df_portfolio_stock_value = df_portfolio_holdings * df_prices_close
    # Calculate the daily portfolio value (sum of stock values and cash)
    df_portfolio_value = df_portfolio_stock_value.sum() + df_portfolio_cash
    #for order in orders:
    #    if "DEPOSIT" in order["action"]:
    #        print 'make deposit: $%s to %s' % (order["shares"],order["symbol"])
    #    if "BUY" in order["action"]:
    #        price =  get_next_open_price(d_data, order["date"], order["symbol"])
    #        print 'BUY %s, %s @%s' % (order["shares"], order["symbol"],price)
    #    if "SELL" idn order["action"]:
    #        price =  get_next_open_price(d_data, order["date"], order["symbol"])
    #        print 'SELL %s, %s, @%s' % (order["shares"], order["symbol"], price)
    return "result"   
    #print "multi-pass portfolio: %s " % (orders)
class Portfolio(object):
    stocks=None
    cash=0
@click.command()
def main():
    orders = []
    y = None
    m = None
    d = None
    symbol = None
    buy_sell = None
    shares = None
    sint = ignore_exception(ValueError)(int)
    sfloat = ignore_exception(ValueError)(float)
    for line in fileinput.input():
        parts = line.split(',')
        if len(parts) >= 6:
            y = sint(parts[0])
            m = sint(parts[1])
            d = sint(parts[2])
            symbol = str(parts[3])
            buy_sell = str(parts[4])
            shares = sfloat(parts[5])
            values = [y, m, d, symbol, buy_sell, shares]
            if all(not x is None for x in values):
                orders.append({"date":datetime(year=y,month=m,day=d), \
                    "symbol":symbol, \
                    "action":buy_sell,"shares":shares})
    process_orders(orders)


if "__main__" in __name__:
    main()