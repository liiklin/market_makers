import sys
import csv
import copy
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.qsdateutil as du
import numpy as np
import pandas as pd

def main():
    analysis_file, benchmark_symbol = validate_input(sys.argv)

    fund, benchmark = analyze(analysis_file, benchmark_symbol)

    print_analysis_results(fund, benchmark, benchmark_symbol)

def validate_input(input_values):
    check_number_params(sys.argv)
    check_csv_file(sys.argv[1])

    return sys.argv[1], sys.argv[2]

def analyze(analysis_file, benchmark_symbol):
    ts_portfolio_value = read_analysis(analysis_file)

    ts_benchmark = read_benchmark_data(ts_portfolio_value.index[0], ts_portfolio_value.index[-1], benchmark_symbol)
    ts_benchmark_close_prices = ts_benchmark['close']

    ts_daily_returns = calculate_daily_returns(ts_portfolio_value)
    ts_cumulative_returns = caculate_cumulative_return(ts_portfolio_value)

    ts_benchmakr_daily_returns = calculate_daily_returns(ts_benchmark_close_prices)
    ts_benchmakr_cumulative_returns = caculate_cumulative_return(ts_benchmark_close_prices)

    benchmark_std_dev, benchmark_avg, benchmark_sharpe = evaluate(ts_benchmakr_daily_returns)
    fund_std_dev, fund_avg, fund_sharpe = evaluate(ts_daily_returns)

    fund_total_return = ts_cumulative_returns.irow(len(ts_cumulative_returns.index)-1)
    benchmark_total_return = ts_benchmakr_cumulative_returns.irow(len(ts_benchmakr_cumulative_returns.index)-1)

    return analysis_result(fund_std_dev, fund_avg, fund_sharpe, fund_total_return), analysis_result(benchmark_std_dev, benchmark_avg, benchmark_sharpe, benchmark_total_return)

class analysis_result:
    def __init__(self, std_dev, avg, sharpe, total_return):
        self.std_dev = std_dev
        self.avg = avg
        self.sharpe = sharpe
        self.total_return = total_return

def check_number_params(input_values):
    if len(input_values) != 3:
        error_msg = 'Incorrect number of input parameters'
        raise ValueError(error_msg)

def check_csv_file(possible_csv_filename):
    if not possible_csv_filename.endswith('.csv'):
        error_msg = 'Not a CSV file: ' + possible_csv_filename
        raise ValueError(error_msg)

def read_analysis(analysis_file):
    reader = csv.reader(open(analysis_file, 'rU'), delimiter=',')
    dates = []
    portfolio_value = []
    for row in reader:
        date = dt.datetime(int(row[0]), int(row[1]), int(row[2]))
        dates.append(date)
        portfolio_value.append(int(row[3].strip()))

    return pd.Series(portfolio_value, index=dates)

def calculate_daily_returns(ts_portfolio_value):
    daily_returns = [0.0]

    for date in ts_portfolio_value.index:
        loc = ts_portfolio_value.index.get_loc(date)

        if loc < np.shape(ts_portfolio_value.index)[0] - 1:
            on_date_value = ts_portfolio_value.irow(loc)
            next_date_value = ts_portfolio_value.irow(loc + 1)
            daily_returns.append((float(next_date_value)/float(on_date_value)) - 1.0)

    return pd.Series(daily_returns, index=ts_portfolio_value.index)

def caculate_cumulative_return(ts_portfolio_value):
    cumulative_returns = [1.0]

    for date in ts_portfolio_value.index:
        loc = ts_portfolio_value.index.get_loc(date)

        if loc > 0:
            cumulative_returns.append(float(ts_portfolio_value.irow(loc))/float(ts_portfolio_value.irow(0)))

    return pd.Series(cumulative_returns, index=ts_portfolio_value.index)

def read_benchmark_data(start_date, end_date, symbol):
    dataobj = da.DataAccess('Yahoo')

    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldt_timestamps = du.getNYSEdays(start_date, end_date + dt.timedelta(days=1) , dt.timedelta(hours=16))

    ldf_data = dataobj.get_data(ldt_timestamps, [symbol], ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))

    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method='ffill')
        d_data[s_key] = d_data[s_key].fillna(method='bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)

    return d_data

def evaluate(ts_daily_returns):
    std_dev = np.std(ts_daily_returns)
    avg = np.average(ts_daily_returns)
    sharpe_ratio = np.sqrt(252) * avg / std_dev

    return std_dev, avg, sharpe_ratio

def print_analysis_results(fund, benchmark, benchmark_symbol):
    print 'Sharpe Ratio of Fund: %.13f' % fund.sharpe
    print 'Sharpe Ratio of %s: %.13f' % (benchmark_symbol, benchmark.sharpe)

    print 'Total Return of Fund: %.13f' % fund.total_return
    print 'Total Return of %s: %.13f' % (benchmark_symbol, benchmark.total_return)

    print 'Standard Deviation of Fund: %.13f' % fund.std_dev
    print 'Standard Deviation of %s: %.13f' % (benchmark_symbol, benchmark.std_dev)

    print 'Average Daily Return of Fund: %.13f' % fund.avg
    print 'Average Daily Return of %s: %.13f' % (benchmark_symbol, benchmark.avg)

if __name__ == '__main__':
    main()