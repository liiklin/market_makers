## Computational Investing I
## HW 4
##
## Author: Michael Schwab
import time
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
    intermediate_results = {}
    def __init__(self, symbol_list, dt_start, dt_end):
        self.logger = logging.getLogger()
        logging.basicConfig()

        self.ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))
        self.dt_index = pd.DatetimeIndex(self.ldt_timestamps)
        self.ls_data = self.load_data(symbol_list)
        self.ls_symbols = self.ls_data["close"].columns
    
    def get_offset_timestamps(self, series, days_offset=5):
        """Utility function for discovering a series of 
        dates that are offset a certain number of market days from the provided 
        series.   The last date is returned if the market date required is not found in 
        self.ldt_timestamps.
        """
        # convert list of datetime to list of timestamps
        #map(lambda d: time.mktime(d.timetuple()),
        series_ts = pd.DatetimeIndex(series)
        # lookup the indexes for the matching timestamps
        index_dates = np.asarray(map(lambda d: self.dt_index.get_loc(d, method="nearest") , series_ts))
        # offset the indexes by 5 (days_offset) days 
        # (the index is in market days so this equates to 5 market days, not calendar days)
        # clamp the index to the last day in case we close to the end
        offset_indexes = [min(x + days_offset, self.dt_index.size -1) for x in index_dates]
        # grab the offset market days by index
        offset_dates = self.dt_index.take(offset_indexes)
        return offset_dates

    def load_data(self, symbols_list):
        """
        Lookup market data for set of signals in the timestamp range
        """
        dataobj = da.DataAccess('Yahoo')
        if not isinstance(symbols_list, list):
            ls_symbols = dataobj.get_symbols_from_list(symbols_list)
        else:
            ls_symbols = symbols_list
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
        self.logger.info("Finding Events...")
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

    def find_events_vectorized(self, t_val, ls_symbols=None, d_data=None, hold_days=5):
        """
        Find events where price yesterday was >= t_val and price today is < t_val.
        This is a vectorized implementation of find events that is ~50x faster than
        a nested loop approach. Typical response times are  < .5 sec for 2 years of 
        events on 500 stocks.
        """
        if not ls_symbols:
            ls_symbols=self.ls_symbols
        if not d_data:
            d_data = self.ls_data
        self.logger.info("Finding Events...")
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
        df_buy_events = pd.DataFrame(events, columns=["symbol"], index=events.index)
        df_buy_events["action"] ="Buy"
        df_buy_events["year"] = events.index.year
        df_buy_events["month"] = events.index.month
        df_buy_events["day"] = events.index.day
        df_buy_events["amount"] = 100
        df_sell_events = pd.DataFrame(events,columns=["symbol"])
        df_sell_events.reset_index()
        df_sell_events.index = sell_days
        #sell_days = df_sell_events.index + timedelta(days=hold_days)
        df_sell_events["action"] ="Sell"
        df_sell_events["year"] = df_sell_events.index.year
        df_sell_events["month"] = df_sell_events.index.month
        df_sell_events["day"] = df_sell_events.index.day
        #df_sell_events.index = sell_days
        df_sell_events["amount"] = 100
        df_orders = df_sell_events.append(df_buy_events).sort_index()
        df_orders.index.name = "date"
        return df_orders
    
    def get_close_prices(self, dt_start,dt_end, ls_symbols):
        dt_timeofday = dt.timedelta(hours=16)
        dataobj = da.DataAccess("Yahoo", verbose=False)
        data = dataobj.get_data(self.ldt_timestamps, ls_symbols, ["close"])
        return data[0]
    
    def generate_order_dates(self, df_orders):
        ts_dates = pd.to_datetime((df_orders.year*10000+df_orders.month*100+df_orders.day).apply(str),format='%Y%m%d')
        return ts_dates

    def simulate(self, df_orders, cash=50000.0):
        df_zeros = pd.DataFrame(0,self.ldt_timestamps, columns=self.ls_symbols)
        # convert buy/sell to - or + order amounts
        df_orders["amount"] = np.where(df_orders["action"].str.upper() =="SELL", (df_orders["amount"] * -1), df_orders["amount"])
        ts_dates = pd.to_datetime((df_orders.year*10000+df_orders.month*100+df_orders.day).apply(str),format='%Y%m%d')
        df = df_orders.copy()
        duped_index = df_orders.index.duplicated()
        self.logger.info("Have %s duplicates" % (sum(duped_index)) )
        df.index.name = "date"
        df.reset_index(inplace=True)
        # index date/symbol/action
        df.set_index(["date","symbol","action"],inplace=True)
        # Group the date/symbol so we have one row/day/symbol
        # if any symbol has both a buy and sell on the same day, 
        # then we will sum it's orders for that day
        # Buys are positive and Sells are negative, so they could negate each other
        df = df.groupby(["date","symbol"]).sum()
        self.intermediate_results["simulate_grouped"] = df
        # pivot the orders and re-apply the date colunn
        # this will give us row dates and a column for each symbol with 
        # order values at the intersects (most will be nan)
        df = df.pivot_table(index=["date"], columns="symbol",values="amount")
        self.intermediate_results["simulate_ordertable"] = df
        
        # create a data frame with rows for each date in range
        # containing the trade values
        df_order_trades = df.combine_first(df_zeros)
        # Calculate the cash value of each trade using close prices
        print "%s prices times %s trades " % (len(self.ls_data["close"]), len(df_order_trades.index))
        print "Missing indexes %s" % ( self.ls_data.index.)
        df_trade_values = df_order_trades * self.ls_data["close"]
        # Calculate the porfolio stock holdings for each day
        df_portfolio_holdings = df_order_trades.cumsum(axis=0)
        self.intermediate_results["simulate_port_hold"] = df_portfolio_holdings
        # Calculate the cash portion of the portfolio
        df_portfolio_cash = cash - (df_trade_values.sum(axis=1).cumsum())
        self.intermediate_results["simulate_port_cash"] = df_portfolio_cash
        # Calcuate the cash value of the portfolio stock holdings
        df_portfolio_stocks_value = df_portfolio_holdings * self.ls_data["close"]
        self.intermediate_results["simulate_stocks_value"] = df_portfolio_stocks_value
        df_portfolio_holdings_value = df_portfolio_stocks_value.sum(axis=1)
        # Calculate the daily portfolio value (sum of stock values and cash)
        df_portfolio_value = df_portfolio_holdings_value + df_portfolio_cash
        df_portfolio_value.name = "portfolio"
        self.intermediate_results["simulate_portfolio"] = df_portfolio_value
        df_ym = pd.DataFrame([{"year":x.year,"month":x.month, "day":x.day} \
            for x in df_portfolio_holdings.index.tolist()], index=df_portfolio_holdings.index)
        df_portfolio_value = df_ym.join(df_portfolio_value)
        return df_portfolio_value
        
    def analyze(self, df_portfolio, out_file=None, days=252):
        start_date = df_portfolio.index[0]
        end_date = df_portfolio.index[-1]
        if out_file:
            df_portfolio[["year","month","day","portfolio"]].to_csv(out_file,header=False,index=False)
        spx_prices = self.get_close_prices(start_date, end_date, ["$SPX"])["$SPX"].values
        spx_ret = tsu.returnize0(spx_prices.copy())
        p_ret = tsu.returnize0(df_portfolio["portfolio"].values.copy())
        print "Details of the Performance of the portfolio :"
        print "Data Range :  %s  to  %s\n" % (start_date, end_date)
        print "Sharpe Ratio of Fund : %s" % (math.sqrt(days) * np.average(p_ret) /np.std(p_ret))
        print "Sharpe Ratio of $SPX : %s\n" % (math.sqrt(days) * spx_ret.mean()/spx_ret.std())
        print "Total Return of Fund :  %s" % (df_portfolio["portfolio"][-1]/df_portfolio["portfolio"][0])
        print "Total Return of $SPX : %s\n" %(spx_prices[-1]/spx_prices[0])
        print "Standard Deviation of Fund :  %s" % (p_ret.std())
        print "Standard Deviation of $SPX : %s\n" % (spx_ret.std())
        print"Average Daily Return of Fund :  %s" % (p_ret.mean())
        print "Average Daily Return of $SPX : %s" % (spx_ret.mean())
        return pd.DataFrame([p_ret,spx_ret], columns=["portfolio","$SPX"], index=df_portfolio )
        

