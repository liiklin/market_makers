## Computational Investing I
## HW 4
##
## Author: Michael Schwab

import pandas as pd
import numpy as np
import math
import copy
import click
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkstudy.EventProfiler as ep
import logging

"""
Accepts a list of symbols along with start and end date
Returns the Event Matrix which is a pandas Datamatrix
Event matrix has the following structure :
    |IBM |GOOG|XOM |MSFT| GS | JP |
(d1)|nan |nan | 1  |nan |nan | 1  |
(d2)|nan | 1  |nan |nan |nan |nan |
(d3)| 1  |nan | 1  |nan | 1  |nan |
(d4)|nan |  1 |nan | 1  |nan |nan |
...................................
...................................
Also, d1 = start date
nan = no information about any event.
1 = status bit(positively confirms the event occurence)
"""

def load_data(ldt_timestamps, symbols_list):
    dataobj = da.DataAccess('Yahoo')
    ls_symbols = dataobj.get_symbols_from_list(symbols_list)
    ls_symbols.append('SPY')

    ls_keys = ['close','actual_close']
    ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))
    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method = 'ffill')
        d_data[s_key] = d_data[s_key].fillna(method = 'bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)
    return d_data

def find_events(ls_symbols, d_data, t_val):
    df_close = d_data['actual_close']
    ts_market = df_close['SPY']

    print "Finding Events..."

    # Creating an empty dataframe
    df_events = copy.deepcopy(df_close)
    df_events = df_events * np.NAN

    # Time stamps for the event range
    ldt_timestamps = df_close.index

    for s_sym in ls_symbols:
        for i in range(1, len(ldt_timestamps)):
            # Calculating the returns for this timestamp
            f_symprice_today = df_close[s_sym].ix[ldt_timestamps[i]]
            f_symprice_yest = df_close[s_sym].ix[ldt_timestamps[i - 1]]
            
            if f_symprice_yest >= float(t_val) and f_symprice_today < float(t_val):
                df_events[s_sym].ix[ldt_timestamps[i]] = 1
    event_rows = df_events.dropna(how="all")
    
    return df_events

def find_events_vectorized(ls_symbols, d_data, t_val):
    print "Finding Events..."
    df_close = d_data['actual_close']
    ts_market = df_close['SPY']
    # Creating an empty dataframe
    df_events = copy.deepcopy(df_close)
    df_events = df_events * np.NAN
    for s_sym in ls_symbols:
        symprice_yesterday = df_close[s_sym].shift(-1)
        df_events[s_sym] = (df_close[s_sym] < t_val) & (symprice_yesterday >= t_val)
        df_events[s_sym] = df_events[s_sym][df_events[s_sym]]
    return df_events

def create_event_orders(df_events, days=5):
    """
    Create buy and sell orders for the detected events
    """
    orders = []
    symbol_events ={}
    event_rows = df_events.dropna(how="all")
    ls_symbols = df_events.columns
    for symbol in ls_symbols:
        events = event_rows[symbol] .dropna(how="all")
        if not events.empty:
            symbol_events[symbol] = events.index
    df_sym_events = pd.DataFrame(events)
    #df_.pivot()
    #orders.append("Need to add some orders...")
    return df_sym_events
