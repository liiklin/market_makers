import pandas as pd
import numpy as np
import math
import sys
import copy
import csv
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil as tsu
#import QSTK.qstkstudy.EventProfiler as ep
# changed to a fixed version of EventProfiler
import EventProfiler as ep
from pandas.tseries.offsets import BDay
import techanalysis as ta

def main():
    dt_start, dt_end, order_file = validate_input()
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))

    dataobj = da.DataAccess('Yahoo')
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']

    ls_2012_symbols = get_symbols_in_year(dataobj, 2012)
    d_2012_data = get_data(dataobj, ldt_timestamps, ls_2012_symbols)

    df_events = find_10_dollar_events(ls_2012_symbols, d_2012_data)
    generate_orders(ls_2012_symbols, df_events, order_file)

def validate_input():
    check_number_params(sys.argv)
    dt_start = check_date(sys.argv[1])
    dt_end = check_date(sys.argv[2])
    output_file = check_csv_file(sys.argv[3])

    return dt_start, dt_end, output_file

def check_number_params(input_values):
    if len(input_values) != 4:
        error_msg = 'Incorrect number of input parameters'
        raise ValueError(error_msg)

def check_date(s_date):
    possible_date = s_date.split(',')
    if len(possible_date) != 3:
        raise ValueError('Incorrect input date %s' % s_date)

    year = int(possible_date[0])
    month = int(possible_date[1])
    day = int(possible_date[2])
    valid_date = dt.datetime(year, month, day)

    return valid_date

def check_csv_file(possible_csv_filename):
    if not possible_csv_filename.endswith('.csv'):
        error_msg = 'Not a CSV file: ' + possible_csv_filename
        raise ValueError(error_msg)

    return possible_csv_filename

def get_symbols_in_year(dataobj, year):
    dataobj = da.DataAccess('Yahoo')

    ls_symbols = dataobj.get_symbols_from_list('sp500' + str(year))
    ls_symbols.append('SPY')

    return ls_symbols

def get_data(dataobj, ldt_timestamps, ls_symbols):
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']

    ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))

    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method='ffill')
        d_data[s_key] = d_data[s_key].fillna(method='bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)

    return d_data

def profile_threshold_actual_close_events(ls_symbols, d_data, actual_close_threshold, filename):
    df_events = find_price_drop_events(ls_symbols, d_data, actual_close_threshold)
    ep.eventprofiler(df_events, d_data, i_lookback=20, i_lookforward=20,
                s_filename=filename, b_market_neutral=True, b_errorbars=True,
                s_market_sym='SPY')

def initialize_event_dataframe(df_orig):
    df_events = copy.deepcopy(df_orig)
    df_events = df_events * np.NAN
    return df_events

def find_price_drop_events(ls_symbols, d_data, actual_close_threshold):
    ''' Finding events when a stock price moved from above the threshold to below the threshold '''
    df_actual_close = d_data['actual_close']

    df_events = initialize_event_dataframe (df_actual_close)

    ldt_timestamps = df_actual_close.index

    for s_sym in ls_symbols:
        for i in range(1, len(ldt_timestamps)):
            # Calculating the actual close price for this timestamp and the day before
            f_actual_close_price_today = df_actual_close[s_sym].ix[ldt_timestamps[i]]
            f_actual_close_price_yest = df_actual_close[s_sym].ix[ldt_timestamps[i - 1]]

            # Event is found if the symbol has a actual close price today below the threshold
            # while the actual close price yesterday was above the threshold
            if f_actual_close_price_today < actual_close_threshold and f_actual_close_price_yest >= actual_close_threshold:
                df_events[s_sym].ix[ldt_timestamps[i]] = 1

    return df_events

def find_5_dollar_events(ls_symbols, d_data):
    ''' Finding events when a stock price moved from above 5$ to below 5$ '''
    return find_price_drop_events(ls_symbols, d_data, 5.0)

def find_6_dollar_events(ls_symbols, d_data):
    ''' Finding events when a stock price moved from above 6$ to below 6$ '''
    return find_price_drop_events(ls_symbols, d_data, 6.0)

def find_7_dollar_events(ls_symbols, d_data):
    ''' Finding events when a stock price moved from above 7$ to below 7$ '''
    return find_price_drop_events(ls_symbols, d_data, 7.0)

def find_8_dollar_events(ls_symbols, d_data):
    ''' Finding events when a stock price moved from above 8$ to below 8$ '''
    return find_price_drop_events(ls_symbols, d_data, 8.0)

def find_9_dollar_events(ls_symbols, d_data):
    ''' Finding events when a stock price moved from above 9$ to below 9$ '''
    return find_price_drop_events(ls_symbols, d_data, 9.0)

def find_10_dollar_events(ls_symbols, d_data):
    ''' Finding events when a stock price moved from above 10$ to below 10$ '''
    return find_price_drop_events(ls_symbols, d_data, 10.0)

def find_bollinger_events(ls_symbols, d_data, stock_bollinger_threshold, spy_bollinger_threshold):
    ''' Finding events when the provided function is triggered '''
    df_close = d_data['close']

    df_events = initialize_event_dataframe(df_close)

    ldt_timestamps = d_data['close'].index

    look_back_days = 20
    spy_bollinger = ta.calculate_bollinger_data(df_close['SPY'], look_back_days)

    for s_sym in ls_symbols:
        sym_bollinger = ta.calculate_bollinger_data(df_close[s_sym], look_back_days)

        for i in range(1, len(ldt_timestamps)):
            if sym_bollinger['bollinger'].ix[ldt_timestamps[i]] <= stock_bollinger_threshold and sym_bollinger['bollinger'].ix[ldt_timestamps[i-1]] >= stock_bollinger_threshold and spy_bollinger['bollinger'].ix[ldt_timestamps[i]] >= spy_bollinger_threshold:
                df_events[s_sym].ix[ldt_timestamps[i]] = 1

    return df_events

def generate_orders(ls_symbols, df_events, order_file):
    file_out = open(order_file, 'w')
    writer = csv.writer(file_out)

    ldt_timestamps = df_events.index
    for i in range(1, len(ldt_timestamps)):
        for s_sym in ls_symbols:
            if df_events[s_sym].ix[ldt_timestamps[i]] == 1:
                buy_date = ldt_timestamps[i]
                sell_date = du.getNextNNYSEdays(buy_date, 6, dt.timedelta(hours=16))[-1]

                writer.writerow(generate_order_line(buy_date, s_sym, 'Buy', 100))
                writer.writerow(generate_order_line(sell_date, s_sym, 'Sell', 100))

    file_out.close()

def generate_order_line(date, s_sym, operation, stocks):
    year = date.year
    month = date.month
    day = date.day
    return [year, month, day, s_sym, operation, stocks]

if __name__ == '__main__':
    main()