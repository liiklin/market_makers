import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd


def load_symbols(symbols = ["AAPL", "GLD", "GOOG", "$SPX", "XOM"]):
    ls_symbols = symbols 
    dt_start = dt.datetime(2010,1,1)
    dt_end = dt.datetime(2010,12,31)
    dt_timeofday = dt.timedelta(hours=16)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)

    c_dataobj = da.DataAccess("Yahoo")
    ls_keys = ["open", "high", "low", "close", "volume", "actual_close" ]
    ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)

    d_data = dict(zip(ls_keys, ldf_data))

    na_price = d_data["close"].values
    na_normalized_price = na_price /na_price[0,:]
    return {"data":na_normalized_price, 
        "timestamps":ldt_timestamps, 
        "ls_symbols":ls_symbols,
        "ylabel":"Adjusted Close (normalized)", 
        "xlabel":"Date"}

def daily_ret(data):
    na_rets = data.copy()
    return tsu.returnize0(na_rets)
    

def save_pdf(d_info, filename="adjustedclose.pdf"):
    
    if not all (x in d_info for x in ["data","timestamps", "ls_symbols"]):
        return None
    else:
        plt.clf()
        plt.plot(d_info["timestamps"], d_info["data"])
        plt.legend(d_info["ls_symbols"])
        plt.ylabel(d_info["ylabel"] if "ylabel" in d_info else "Adjusted Close (normalized")
        plt.xlabel( d_info["xlabel"] if "xlabel" in d_info else "Date")
        plt.savefig(filename, format="pdf")

if "__main__" in __name__:
    symb_info = load_symbols()
    save_pdf(symb_info)
    dr_info =  load_symbols(symbols=["XOM", "$SPX"])
    dr_info["data"] = daily_ret(dr_info["data"])
    dr_info["ylabel"] = "Daily Returns"
    save_pdf(dr_info, filename="dailyreturns.pdf")

