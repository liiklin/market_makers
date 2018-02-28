import fileinput
import click
import numpy as np

from datetime import datetime
from datetime import timedelta
from operator import itemgetter
import logging
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
    
def get_close_prices(dt_start,dt_end, ls_symbols):
    dt_timeofday = dt.timedelta(hours=16)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)
    dataobj = da.DataAccess("Yahoo", verbose=False)
    data = dataobj.get_data(ldt_timestamps, ls_symbols, ["close"])
    return data[0]

def process_orders(df_orders, initial_cash=10000.0,custom_enddate=None):
    if not isinstance(initial_cash, float):
        print ("initial_case must be a float")
        return None
    if not isinstance(df_orders, pd.DataFrame):
        print ("df_orders must be a DataFrame")
        return None
    add_16h = lambda dt: dt + timedelta(hours=16) 
    df_orders["date"] = map(add_16h, df_orders["date"])
    df_orders = df_orders.set_index("date")
    ls_symbols = list(df_orders.columns.values)
    dt_start = df_orders.index[0] # + dt.timedelta(days=-1)
    dt_end = df_orders.index[-1] if custom_enddate is None else custom_enddate
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))
    after_hrs_order_dates = np.setdiff1d(df_orders.index.tolist(), ldt_timestamps)
    if after_hrs_order_dates.any():
        ldt_timestamps.extend(after_hrs_order_dates)
    dataobj = da.DataAccess("Yahoo", verbose=False)
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys, verbose=False)
    for d in ldf_data:
        d.fillna(method="pad")
        d.fillna(method="bfill")
    d_data = dict(zip(ls_keys, ldf_data))
    df_prices_close = d_data["close"]
    df_zeros = pd.DataFrame(0,ldt_timestamps, columns=ls_symbols)
    # drop any orders not on trading days
    #df_order_wrong_day = df_orders[~df_orders.index.isin(df_zeros.index)]
    #print ("Dropping Orders on Market Closed Days...")
    #print (df_order_wrong_day)
    #df_orders.drop(df_order_wrong_day.index, inplace=True)
    # create a data frame with rows for each date in range
    # containing the trade values
    df_order_trades = df_orders.combine_first(df_zeros)
    # Calculate the cash value of each trade using close prices
    df_trade_values = df_order_trades * df_prices_close
    # Calculate the porfolio stock holdings for each day
    df_portfolio_holdings = df_order_trades.cumsum(axis=0)
    # Calculate the cash portion of the portfolio
    df_portfolio_cash = initial_cash - (df_trade_values.sum(axis=1).cumsum())
    # Calcuate the cash value of the portfolio stock holdings
    df_portfolio_stocks_value = df_portfolio_holdings * df_prices_close
    df_portfolio_holdings_value = df_portfolio_stocks_value.sum(axis=1)

    # Calculate the daily portfolio value (sum of stock values and cash)
    df_portfolio_value = df_portfolio_holdings_value + df_portfolio_cash
    df_portfolio_value.name = "portfolio"
    df_ym = pd.DataFrame([{"year":x.year,"month":x.month, "day":x.day} \
        for x in df_portfolio_holdings.index.tolist()], index=df_portfolio_holdings.index)
    df_portfolio_value = df_ym.join(df_portfolio_value)
    return df_portfolio_value

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