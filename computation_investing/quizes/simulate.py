import pandas as pd
pd.TimeSeries = pd.Series
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import datetime as dt


def simulate(dt_start, dt_end, ls_symbols, allocations):
    """
    outputs:
        - stadard deviation of returns
        - average daily returns
        - sharpe ratio 
        - cumulative return of portfolio
        data : dict of keys (ie close, vol, open etc) 
        where each value is a data fram
    """
    daily_ret_weighted = lambda s, a: (data["close"][s].shift(1) / data["close"][s] -1) * a
    
    portfolio_stdev_ret = 0
    avg_daily_ret = 0
    sharpe = 0
    cum_ret = 0

    dt_timeofday = dt.timedelta(hours=16)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)
    data = get_data(ldt_timestamps, ls_symbols, ["close","vol"])
    d_allocations = dict(zip(ls_symbols, allocations))
    daily_returns_weighted = dict((symbol, \
        daily_ret_weighted(symbol, d_allocations[symbol])) \
        for symbol in ls_symbols)
    df_drw =  pd.DataFrame(daily_returns_weighted).dropna()
    portfolio_returns = df_drw.loc[:, :].sum(axis=1)
    portfolio_stdev_ret = float(portfolio_returns.std())
    cum_ret = float(portfolio_returns.sum())
    avg_daily_ret = float(cum_ret/float(df_drw.count()[0]) )
    sharpe = float(tsu.get_sharpe_ratio(portfolio_returns))
    return (portfolio_stdev_ret, avg_daily_ret, sharpe, cum_ret)

def get_data(ldt_timestamps, ls_symbols, ls_keys ):
    
    c_dataobj = da.DataAccess("Yahoo")
    ls_keys = ["open", "high", "low", "close", "volume", "actual_close" ]
    ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)

    d_data = dict(zip(ls_keys, ldf_data))
    return d_data

