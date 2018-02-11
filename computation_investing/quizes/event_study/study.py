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
import QSTK.qstkstudy.Events as ev
import datetime as dt
import QSTK.qstkstudy.EventProfiler as ep
import numpy as np


@click.command()
@click.option("--sym_file")
@click.option("--year")
def study_five(sym_file, year):
    ls_symbols = np.loadtxt(sym_file,dtype='S10',comments='#')
    print len(ls_symbols), " symbols loaded."
    dt_start = dt.datetime(int(year) - 1,1,1)
    dt_end = dt.datetime(int(year),12,31)
    ldt_timestamps = du.getNYSEdays( dt_start, dt_end, dt.timedelta(hours=16) )

    dataobj = da.DataAccess('Yahoo')
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    print "Got data"
    d_data = dict(zip(ls_keys, ldf_data))
    print "Searching events..."
    eventMatrix = ev.find_drop_below_five(ls_symbols,d_data,verbose=True)
    ep.eventprofiler(eventMatrix, d_data,
            i_lookback=20,i_lookforward=20,
            s_filename="drop_below_five.pdf")

    
if __name__ == '__main__':
    study_five()
    