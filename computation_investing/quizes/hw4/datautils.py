import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.DataAccess as da
import datetime as dt

def get_data(dt_start, dt_end, ls_symbols):
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))

    dataobj = da.DataAccess('Yahoo')

    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']

    ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))

    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method='ffill')
        d_data[s_key] = d_data[s_key].fillna(method='bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)

    return d_data

def get_symbols_in_year(year):
    dataobj = da.DataAccess('Yahoo')

    ls_symbols = dataobj.get_symbols_from_list('sp500' + str(year))
    ls_symbols.append('SPY')

    return ls_symbols
    