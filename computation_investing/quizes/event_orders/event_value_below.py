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
from  datetime import timedelta
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
class EventOrders(object):
    def __init__(self, dt_start, dt_end):
        self.ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))
    
    def get_offset_timestamps(self, series, days_offset=5):
        """Utility function for discovering a series of 
        dates that are offset a certain number of market days from the provided 
        series.   The last date is returned if the market date required is not found in 
        self.ldt_timestamps.
        """
        matching_locs = self.ldt_timestamps.index.get_loc(series)
        return matching_locs

    def load_data(self, symbols_list):
        """
        Lookup market data for set of signals in the timestamp range
        """
        dataobj = da.DataAccess('Yahoo')
        ls_symbols = dataobj.get_symbols_from_list(symbols_list)
        ls_symbols.append('SPY')

        ls_keys = ['close','actual_close']
        ldf_data = dataobj.get_data(self.ldt_timestamps, ls_symbols, ls_keys)
        d_data = dict(zip(ls_keys, ldf_data))
        for s_key in ls_keys:
            d_data[s_key] = d_data[s_key].fillna(method = 'ffill')
            d_data[s_key] = d_data[s_key].fillna(method = 'bfill')
            d_data[s_key] = d_data[s_key].fillna(1.0)
        return d_data

    def find_events(self, ls_symbols, d_data, t_val):
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
        symbol_events = {}
        for s_sym in ls_symbols:
            events = df_events[s_sym].dropna(how="all")
            if not events.empty:
                symbol_events[s_sym] = events.index
        df_events = pd.DataFrame(symbol_events)
        return df_events

    def find_events_vectorized(self, ls_symbols, d_data, t_val, hold_days=5):
        """
        Find events where price yesterday was >= t_val and price today is < t_val.
        This is a vectorized implementation of find events that is ~50x faster than
        a nested loop approach. Typical response times are  < .5 sec for 2 years of 
        events on 500 stocks.
        """
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
        event_rows = df_events.dropna(how="all")
        symbol_events = {}
        event_series = pd.Series([])
        dates = []
        symbols = []
        for s_sym in ls_symbols:
            events = df_events[s_sym].dropna(how="all")
            dates.extend(events.index)
            symbols.extend([s_sym] * len(events.index))
        return pd.Series(symbols,dates).sort_index()

    def create_event_orders(self, events, sell_days, hold_days=5, amount=100):
        """
        Create buy and sell orders for the detected events.
        """
        df_buy_events = pd.DataFrame(events, columns=["stock"], index=events.index)
        df_buy_events["order"] ="Buy"
        df_buy_events["year"] = events.index.year
        df_buy_events["month"] = events.index.month
        df_buy_events["day"] = events.index.day
        df_buy_events["amount"] = 100
        df_sell_events = pd.DataFrame(events,columns=["stock"])
        df_sell_events.reset_index()
        df_sell_events.index = sell_days[0:events.shape(0)]
        #sell_days = df_sell_events.index + timedelta(days=hold_days)
        df_sell_events["order"] ="Sell"
        df_sell_events["year"] = df_sell_events.index.year
        df_sell_events["month"] = df_sell_events.index.sell_days.month
        df_sell_events["day"] = df_sell_events.index.sell_days.day
        #df_sell_events.index = sell_days
        df_sell_events["amount"] = 100
        df_orders = df_sell_events.append(df_buy_events).sort_index()
        return df_orders

