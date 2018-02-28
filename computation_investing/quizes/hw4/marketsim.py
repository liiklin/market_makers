import sys
import csv
import copy
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.qsdateutil as du
import numpy as np
import pandas as pd

def main():
    cash, order_file, analysis_file = validate_input(sys.argv)

    simulation_result = simulate(cash, order_file)

    write_simulation_result(simulation_result, analysis_file)

def simulate(cash, order_file):
    dates, symbols = read_orders(order_file)

    init_date, end_date = dates[0], dates[-1]
    data = read_data(dates[0], dates[-1], symbols)

    trade_matrix = create_trade_matrix(order_file, dates[0], dates[-1], symbols)

    cash_matrix = create_cash_matrix(dates[0], dates[-1], cash, symbols, trade_matrix, data)

    holding_matrix = create_holding_matrix(dates[0], dates[-1], symbols, trade_matrix)

    value_matrix = create_value_matrix(holding_matrix, data)

    portfolio_value = create_portfolio_value(value_matrix, cash_matrix)

    append_column_sufix(holding_matrix, symbols, '_stocks')
    append_column_sufix(value_matrix, symbols, '_value')

    return pd.concat([trade_matrix, holding_matrix, cash_matrix, value_matrix, portfolio_value], axis=1)

def validate_input(input_values):
    check_number_params(sys.argv)
    check_cash(sys.argv[1])
    check_csv_file(sys.argv[2])
    check_csv_file(sys.argv[3])

    return sys.argv[1], sys.argv[2], sys.argv[3]

def check_number_params(input_values):
    if len(input_values) != 4:
        error_msg = 'Incorrect number of input parameters'
        raise ValueError(error_msg)

def check_cash(possible_cash_value):
    if not possible_cash_value.isdigit():
        error_msg = 'Initial cash value is incorrect: ' + str(possible_cash_value)
        raise ValueError(error_msg)

def check_csv_file(possible_csv_filename):
    if not possible_csv_filename.endswith('.csv'):
        error_msg = 'Not a CSV file: ' + possible_csv_filename
        raise ValueError(error_msg)

def read_orders(order_file):
    reader = csv.reader(open(order_file, 'rU'), delimiter=',')
    dates = []
    symbols = []
    for row in reader:
        date = dt.datetime(int(row[0]), int(row[1]), int(row[2]))
        dates.append(date)
        symbols.append(row[3].strip())

    dates = list(set(dates))
    symbols = list(set(symbols))

    dates.sort()
    symbols.sort()

    return dates, symbols

def read_data(dt_start, dt_end, ls_symbols):
    dataobj = da.DataAccess('Yahoo')

    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end + dt.timedelta(days=1), dt.timedelta(hours=16))

    ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))

    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method='ffill')
        d_data[s_key] = d_data[s_key].fillna(method='bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)

    return d_data

def create_trade_matrix(order_file, init_date, end_date, symbols):
    dates = du.getNYSEdays(init_date, end_date + dt.timedelta(days=1) , dt.timedelta(hours=16))
    
    trade_matrix = pd.DataFrame(data=np.zeros((len(dates), len(symbols))), index=dates, columns=symbols)

    reader = csv.reader(open(order_file, 'rU'), delimiter=',')
    for row in reader:
        date = dt.datetime(int(row[0]), int(row[1]), int(row[2])) + dt.timedelta(hours=16)
        symbol = row[3].strip()
        num_stocks = row[5].strip()
        if row[4].strip().lower() == 'buy':
            trade_matrix[symbol][date] = trade_matrix[symbol][date] + int(num_stocks)
        if row[4].strip().lower() == 'sell':
            trade_matrix[symbol][date] = trade_matrix[symbol][date] - int(num_stocks)

    return trade_matrix

def create_cash_matrix(init_date, end_date, initial_cash, symbols, trade_matrix, data):
    adjusted_close_prices = data['close']

    dates = du.getNYSEdays(init_date, end_date + dt.timedelta(days=1) , dt.timedelta(hours=16))

    cash_array = ['cash']
    cash_data = np.empty((len(dates), len(cash_array)))
    cash_data.fill(np.nan)
    cash_matrix = pd.DataFrame(data=cash_data, index=dates, columns=cash_array)

    cash_matrix['cash'][dates[0]] = initial_cash


    prev_date = init_date + dt.timedelta(hours=16)
    for date in dates:
        for symbol in symbols:
            stocks = trade_matrix[symbol][date]
            stock_price = adjusted_close_prices[symbol][date]

            if np.isnan(cash_matrix['cash'][date]):
                cash_matrix['cash'][date] = cash_matrix['cash'][prev_date] - (stocks * stock_price)
            else:
                cash_matrix['cash'][date] = cash_matrix['cash'][date] - (stocks * stock_price)

            prev_date = date

    return cash_matrix

def create_holding_matrix(init_date, end_date, symbols, trade_matrix):
    dates = du.getNYSEdays(init_date, end_date + dt.timedelta(days=1) , dt.timedelta(hours=16))

    holding_data = np.empty((len(dates), len(symbols)))
    holding_data.fill(np.nan)
    holding_matrix = pd.DataFrame(data=holding_data, index=dates, columns=symbols)

    for symbol in symbols:
        prev_date = dates[0]
        for date in dates:
            stocks = trade_matrix[symbol][date]

            if date == prev_date:
                holding_matrix[symbol][date] = trade_matrix[symbol][prev_date]
            else:
                holding_matrix[symbol][date] = holding_matrix[symbol][prev_date] + stocks
            prev_date = date

    return holding_matrix

def create_value_matrix(holding_matrix, data):
    adjusted_close_prices = data['close']

    return adjusted_close_prices.multiply(holding_matrix)

def create_portfolio_value(value_matrix, cash_matrix):
    portfolio_value = pd.concat([cash_matrix, value_matrix], axis=1).sum(axis=1).to_frame()
    portfolio_value.columns = ['portfolio_value']
    return portfolio_value

def append_column_sufix(dataframe, columns, sufix):
    new_columns = []
    for column in columns:
        new_columns.append(column + sufix)
    dataframe.columns = new_columns

def write_simulation_result(simulation_result, analysis_file):
    with open(analysis_file, 'wb') as analysis:
        for index in simulation_result.index:
            year, month, day = index.year, index.month, index.day
            csv_analysis = csv.writer(analysis, delimiter=',')
            csv_analysis.writerow([year, month, day, int(round(simulation_result['portfolio_value'][index]))])

if __name__ == '__main__':
    main()