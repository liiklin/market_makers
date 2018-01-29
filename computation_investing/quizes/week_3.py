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
    """
    std_ret = 0
    avg_daily_ret = 0
    sharpe_ratio = 0
    cumm_ret = 0
    dt_timeofday = dt.timedelta(hours=16)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)
    data = get_data(ldt_timestamps, ls_symbols, ["close"])
    
    return (std_ret, avg_daily_ret, sharpe_ratio, cumm_ret)
def get_data(ldt_timestamps, ls_symbols, ls_keys ):
    
    c_dataobj = da.DataAccess("Yahoo")
    ls_keys = ["open", "high", "low", "close", "volume", "actual_close" ]
    ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)

    d_data = dict(zip(ls_keys, ldf_data))
