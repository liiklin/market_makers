import analyze as an
import events as ev
import datetime as dt
import marketsim as mksim
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.DataAccess as da

def question1():
    q = """
    The event is defined as when the actual close of the stock price drops below $6.00, more specifically, when:
    price[t-1]>=6.0 and price[t]<6.0 an event has occurred on date t.
    * Test this event using the Event Profiler over the period from 1st Jan, 2008 to 31st Dec 2009.
    * Using the symbol list - SP5002012
    * Starting Cash: $50,000
    * At every event Buy 100 shares of the equity, and Sell them 5 trading days later. In case not enough days are available Sell them on the last trading day. (Similar to what the homework 4 description wanted).
    * Run this in your simulator and analyze the results.
    What is the sharpe ratio of the fund ?
    * 0.45 to 0.55
    * 0.55 to 0.65
    * 0.75 to 0.85
    * 0.65 to 0.75
    """

    dt_start = dt.datetime(2008, 1, 1)
    dt_end = dt.datetime(2009, 12, 31)
    cash = 50000

    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))
    dataobj = da.DataAccess('Yahoo')
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']

    ls_2012_symbols = ev.get_symbols_in_year(dataobj, 2012)
    d_2012_data = ev.get_data(dataobj, ldt_timestamps, ls_2012_symbols)

    order_file = 'orders.csv'
    analysis_file = 'values_6_dollar_event.csv'
    benchmark_symbol = '$SPX'

    df_events = ev.find_6_dollar_events(ls_2012_symbols, d_2012_data)
    ev.generate_orders(ls_2012_symbols, df_events, order_file)

    simulation_result = mksim.simulate(cash, order_file)
    mksim.write_simulation_result(simulation_result, analysis_file)

    fund, benchmark = an.analyze(analysis_file, benchmark_symbol)

    return q, fund.sharpe

def question2():
    q = """
    The event is defined as when the actual close of the stock price drops below $7.00, more specifically, when:
    price[t-1]>=7.0 and price[t]<7.0 an event has occurred on date t.
    * Test this event using the Event Profiler over the period from 1st Jan, 2008 to 31st Dec 2009.
    * Using the symbol list - SP5002012
    * Starting Cash: $50,000
    * At every event Buy 100 shares of the equity, and Sell them 5 trading days later. In case not enough days are available Sell them on the last trading day. (Similar to what the homework 4 description wanted).
    * Run this in your simulator and analyze the results.
    What is the sharpe ratio of the fund ?
    * 0.8 to 0.9
    * 0.6 to 0.7
    * 0.7 to 0.8
    * 0.9 to 1.0
    """

    dt_start = dt.datetime(2008, 1, 1)
    dt_end = dt.datetime(2009, 12, 31)
    cash = 50000

    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))
    dataobj = da.DataAccess('Yahoo')
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']

    ls_2012_symbols = ev.get_symbols_in_year(dataobj, 2012)
    d_2012_data = ev.get_data(dataobj, ldt_timestamps, ls_2012_symbols)

    order_file = 'orders.csv'
    analysis_file = 'values_7_dollar_event.csv'
    benchmark_symbol = '$SPX'

    df_events = ev.find_7_dollar_events(ls_2012_symbols, d_2012_data)
    ev.generate_orders(ls_2012_symbols, df_events, order_file)

    simulation_result = mksim.simulate(cash, order_file)
    mksim.write_simulation_result(simulation_result, analysis_file)

    fund, benchmark = an.analyze(analysis_file, benchmark_symbol)

    return q, fund.sharpe

def question3():
    q = """
    The event is defined as when the actual close of the stock price drops below $8.00, more specifically, when:
    price[t-1]>=8.0 and price[t]<8.0 an event has occurred on date t.
    * Test this event using the Event Profiler over the period from 1st Jan, 2008 to 31st Dec 2009.
    * Using the symbol list - SP5002012
    * Starting Cash: $50,000
    * At every event Buy 100 shares of the equity, and Sell them 5 trading days later. In case not enough days are available Sell them on the last trading day. (Similar to what the homework 4 description wanted).
    * Run this in your simulator and analyze the results.
    What is the sharpe ratio of the fund ?
    * 1.15 to 1.25
    * 0.95 to 1.05
    * 0.85 to 0.95
    * 1.05 to 1.15
    """

    dt_start = dt.datetime(2008, 1, 1)
    dt_end = dt.datetime(2009, 12, 31)
    cash = 50000

    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))
    dataobj = da.DataAccess('Yahoo')
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']

    ls_2012_symbols = ev.get_symbols_in_year(dataobj, 2012)
    d_2012_data = ev.get_data(dataobj, ldt_timestamps, ls_2012_symbols)

    order_file = 'orders.csv'
    analysis_file = 'values_8_dollar_event.csv'
    benchmark_symbol = '$SPX'

    df_events = ev.find_8_dollar_events(ls_2012_symbols, d_2012_data)
    ev.generate_orders(ls_2012_symbols, df_events, order_file)

    simulation_result = mksim.simulate(cash, order_file)
    mksim.write_simulation_result(simulation_result, analysis_file)

    fund, benchmark = an.analyze(analysis_file, benchmark_symbol)

    return q, fund.sharpe

def question4():
    q = """
    4.
    The event is defined as when the actual close of the stock price drops below $9.00, more specifically, when:
    price[t-1]>=9.0 and price[t]<9.0 an event has occurred on date t.
    * Test this event using the Event Profiler over the period from 1st Jan, 2008 to 31st Dec 2009.
    * Using the symbol list - SP5002012
    * Starting Cash: $50,000
    * At every event Buy 100 shares of the equity, and Sell them 5 trading days later. In case not enough days are available Sell them on the last trading day. (Similar to what the homework 4 description wanted).
    * Run this in your simulator and analyze the results.
    What is the sharpe ratio of the fund ?
    * 1.0 to 1.1
    * 0.9 to 1.0
    * 0.8 to 0.9
    * 0.7 to 0.8
    """

    dt_start = dt.datetime(2008, 1, 1)
    dt_end = dt.datetime(2009, 12, 31)
    cash = 50000

    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))
    dataobj = da.DataAccess('Yahoo')
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']

    ls_2012_symbols = ev.get_symbols_in_year(dataobj, 2012)
    d_2012_data = ev.get_data(dataobj, ldt_timestamps, ls_2012_symbols)

    order_file = 'orders.csv'
    analysis_file = 'values_9_dollar_event.csv'
    benchmark_symbol = '$SPX'

    df_events = ev.find_9_dollar_events(ls_2012_symbols, d_2012_data)
    ev.generate_orders(ls_2012_symbols, df_events, order_file)

    simulation_result = mksim.simulate(cash, order_file)
    mksim.write_simulation_result(simulation_result, analysis_file)

    fund, benchmark = an.analyze(analysis_file, benchmark_symbol)

    return q, fund.sharpe

def question5():
    q = """
    The event is defined as when the actual close of the stock price drops below $10.00, more specifically, when:
    price[t-1]>=10.0 and price[t]<10.0 an event has occurred on date t.
    * Test this event using the Event Profiler over the period from 1st Jan, 2008 to 31st Dec 2009.
    * Using the symbol list - SP5002012
    * Starting Cash: $50,000
    * At every event Buy 100 shares of the equity, and Sell them 5 trading days later. In case not enough days are available Sell them on the last trading day. (Similar to what the homework 4 description wanted).
    * Run this in your simulator and analyze the results.
    What is the sharpe ratio of the fund ?
    * 0.45 to 0.55
    * 0.75 to 0.85
    * 0.55 to 0.65
    * 0.65 to 0.75
    """

    dt_start = dt.datetime(2008, 1, 1)
    dt_end = dt.datetime(2009, 12, 31)
    cash = 50000

    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))
    dataobj = da.DataAccess('Yahoo')
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']

    ls_2012_symbols = ev.get_symbols_in_year(dataobj, 2012)
    d_2012_data = ev.get_data(dataobj, ldt_timestamps, ls_2012_symbols)

    order_file = 'orders.csv'
    analysis_file = 'values_10_dollar_event.csv'
    benchmark_symbol = '$SPX'

    df_events = ev.find_10_dollar_events(ls_2012_symbols, d_2012_data)
    ev.generate_orders(ls_2012_symbols, df_events, order_file)

    simulation_result = mksim.simulate(cash, order_file)
    mksim.write_simulation_result(simulation_result, analysis_file)

    fund, benchmark = an.analyze(analysis_file, benchmark_symbol)

    return q, fund.sharpe

def question6():
    q = """
    The event is defined as when the actual close of the stock price drops below $6.00, more specifically, when:
    price[t-1]>=6.0 and price[t]<6.0 an event has occurred on date t.
    * Test this event using the Event Profiler over the period from 1st Jan, 2008 to 31st Dec 2009.
    * Using the symbol list - SP5002012
    * Starting Cash: $50,000
    * At every event Buy 100 shares of the equity, and Sell them 5 trading days later. In case not enough days are available Sell them on the last trading day. (Similar to what the homework 4 description wanted).
    * Run this in your simulator and analyze the results.
    What is the total return of the fund ?
    * 1.3 to 1.4
    * 1.4 to 1.5
    * 1.2 to 1.3
    * 1.1 to 1.2
    """

    analysis_file = 'values_6_dollar_event.csv'
    benchmark_symbol = '$SPX'

    fund, benchmark = an.analyze(analysis_file, benchmark_symbol)

    return q, fund.total_return

def question7():
    q = """
    The event is defined as when the actual close of the stock price drops below $7.00, more specifically, when:
    price[t-1]>=7.0 and price[t]<7.0 an event has occurred on date t.
    * Test this event using the Event Profiler over the period from 1st Jan, 2008 to 31st Dec 2009.
    * Using the symbol list - SP5002012
    * Starting Cash: $50,000
    * At every event Buy 100 shares of the equity, and Sell them 5 trading days later. In case not enough days are available Sell them on the last trading day. (Similar to what the homework 4 description wanted).
    * Run this in your simulator and analyze the results.
    What is the total return of the fund ?
    * 1.35 to 1.45
    * 1.05 to 1.15
    * 1.25 to 1.35
    * 1.15 to 1.25
    """

    analysis_file = 'values_7_dollar_event.csv'
    benchmark_symbol = '$SPX'

    fund, benchmark = an.analyze(analysis_file, benchmark_symbol)

    return q, fund.total_return

def question8():
    q = """
    The event is defined as when the actual close of the stock price drops below $8.00, more specifically, when:
    price[t-1]>=8.0 and price[t]<8.0 an event has occurred on date t.
    * Test this event using the Event Profiler over the period from 1st Jan, 2008 to 31st Dec 2009.
    * Using the symbol list - SP5002012
    * Starting Cash: $50,000
    * At every event Buy 100 shares of the equity, and Sell them 5 trading days later. In case not enough days are available Sell them on the last trading day. (Similar to what the homework 4 description wanted).
    * Run this in your simulator and analyze the results.
    What is the total return of the fund ?
    * 1.25 to 1.35
    * 1.35 to 1.45
    * 1.15 to 1.25
    * 1.05 to 1.25
    """

    analysis_file = 'values_8_dollar_event.csv'
    benchmark_symbol = '$SPX'

    fund, benchmark = an.analyze(analysis_file, benchmark_symbol)

    return q, fund.total_return

def question9():
    q = """
    The event is defined as when the actual close of the stock price drops below $9.00, more specifically, when:
    price[t-1]>=9.0 and price[t]<9.0 an event has occurred on date t.
    * Test this event using the Event Profiler over the period from 1st Jan, 2008 to 31st Dec 2009.
    * Using the symbol list - SP5002012
    * Starting Cash: $50,000
    * At every event Buy 100 shares of the equity, and Sell them 5 trading days later. In case not enough days are available Sell them on the last trading day. (Similar to what the homework 4 description wanted).
    * Run this in your simulator and analyze the results.
    What is the total return of the fund ?
    * 0.9 to 1.0
    * 1.0 to 1.1
    * 1.1 to 1.2
    * 1.2 to 1.3
    """

    analysis_file = 'values_9_dollar_event.csv'
    benchmark_symbol = '$SPX'

    fund, benchmark = an.analyze(analysis_file, benchmark_symbol)

    return q, fund.total_return

def question10():
    q = """
    The event is defined as when the actual close of the stock price drops below $10.00, more specifically, when:
    price[t-1]>=10.0 and price[t]<10.0 an event has occurred on date t.
    * Test this event using the Event Profiler over the period from 1st Jan, 2008 to 31st Dec 2009.
    * Using the symbol list - SP5002012
    * Starting Cash: $50,000
    * At every event Buy 100 shares of the equity, and Sell them 5 trading days later. In case not enough days are available Sell them on the last trading day. (Similar to what the homework 4 description wanted).
    * Run this in your simulator and analyze the results.
    What is the total return of the fund ?
    * 1.15 to 1.25
    * 1.25 to 1.35
    * 1.05 to 1.15
    * 1.35 to 1.45
    """

    analysis_file = 'values_10_dollar_event.csv'
    benchmark_symbol = '$SPX'

    fund, benchmark = an.analyze(analysis_file, benchmark_symbol)

    return q, fund.total_return

def main():
    questions = [question1, question2, question3, question4, question5, question6, question7, question8, question9, question10]
    for i in range(0, 10):
        q, ans = questions[i]()
        print '==========================='
        print q
        print ans

if __name__ == '__main__':
    main()