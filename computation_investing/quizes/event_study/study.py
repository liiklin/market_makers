#
# Example use of the event profiler
#
# Modern pandas overrides
import pandas as pd
pd.TimeSeries = pd.Series

import click
import os
# QSTK Imports
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.DataAccess as da
from Events import find_drop_below_five
import datetime as dt
from EventProfiler import eventprofiler
import numpy as np


@click.command()
@click.option("--sym_file")
@click.option("--year")
@click.option("--head")
def study_five(sym_file, year, head=None):
    ls_symbols = np.loadtxt(sym_file,dtype='S10',comments='#')
    if head:
        ls_symbols = ls_symbols[0:int(head)-1]
        if not "SPY" in ls_symbols:
            ls_symbols = np.append(ls_symbols,["SPY"])
    print len(ls_symbols), " symbols loaded."
    dt_start = dt.datetime(int(year) - 1,1,1)
    dt_end = dt.datetime(int(year),12,31)
    ldt_timestamps = du.getNYSEdays( dt_start, dt_end, dt.timedelta(hours=16) )
    print "Got data for %s to %s" % (dt_start, dt_end)
    dataobj = da.DataAccess('Yahoo')
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    #print "Got data"
    d_data = dict(zip(ls_keys, ldf_data))
    print "Searching events..."
    try:
        eventMatrix = find_drop_below_five(ls_symbols,d_data,verbose=True)
        eventprofiler(eventMatrix, d_data,
            i_lookback=20,i_lookforward=20,
            s_filename="drop_below_five.pdf")
    except Exception as e:
        print e

    
if __name__ == '__main__':
    study_five()
    