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
    portfolio_stdev_ret = 0
    avg_daily_ret = 0
    sharpe = 0
    cum_ret = 0

    dt_timeofday = dt.timedelta(hours=16)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)
    data = get_data(ldt_timestamps, ls_symbols, ["close","vol"])
    d_allocations = dict(zip(ls_symbols, allocations))
    # for each day,the weighted sum of the returns of all stocks

    #  calculate the portfolio return to date

    price = data["close"].values
    normalized_price = (price/price[0,:])
    normalized_prices = normalized_price.copy()
    #daily_returns = tsu.returnize1(na_returns)
    daily_returns = normalized_prices
    
    #df_cum =  pd.DataFrame(cum_returns, index=ldt_timestamps, columns=ls_symbols)
    df_dr = pd.DataFrame(daily_returns, index=ldt_timestamps, columns=ls_symbols)
    df_dr.to_csv("/home/mcstar/daily_returns_cum.csv")     
    portfolio_dr = pd.DataFrame()
    portfolio_cum = pd.DataFrame()

    for symbol in ls_symbols:
        portfolio_dr[symbol] = (df_dr[symbol]) * d_allocations[symbol]

    portfolio_dr["ret"] = portfolio_dr.sum(axis=1)
    ret = portfolio_dr["ret"].copy()
    portfolio_dr["daily_ret"] = tsu.returnize0(ret)
    #portfolio_dr["ret_cum"] = (1+ portfolio_dr["ret"]).cumprod() -1 
    
    portfolio_dr.to_csv("/home/mcstar/portfolio.csv")
    portfolio_stdev_ret = float(portfolio_dr["daily_ret"].std())
    cum_ret = float(portfolio_dr["ret"].iloc[-1])
    avg_daily_ret = float(portfolio_dr["daily_ret"].mean())
    sharpe = float(tsu.get_sharpe_ratio(portfolio_dr["daily_ret"]))
    return (portfolio_stdev_ret, avg_daily_ret, sharpe, cum_ret)

def get_data(ldt_timestamps, ls_symbols, ls_keys ):
    
    c_dataobj = da.DataAccess("Yahoo")
    ls_keys = ["open", "high", "low", "close", "volume", "actual_close" ]
    ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)

    d_data = dict(zip(ls_keys, ldf_data))
    return d_data

