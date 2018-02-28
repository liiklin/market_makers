from __future__ import print_function
import unittest
import simulate
from datetime import datetime


timeFormat = '%Y-%m-%dT%H:%M:%S'

class TestSimulate(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_simulate_simple(self):
        print ("Start Simulate Simple")
        allocations = [.2,.3]
        allocations.append(1 - sum(allocations))
        result = simulate.simulate(self.formatTimeString("2010-1-1T00:00:00"), \
            self.formatTimeString("2010-3-1T00:00:00"), \
            ["GOOG","$SPX","XOM"], \
            allocations)
        self.assertIsNotNone(result)
        print("simulate test result : %s" % (str(result)))
        
    def test_example_1(self):
        dt_start = datetime(2011,1,1)
        dt_end = datetime(2011, 12, 31)
        symbols = ["AAPL","GLD","GOOG","XOM"]
        allocations = [.4, .4, 0, .2]
        vol, daily_ret, sharpe, cum_ret = simulate.simulate(\
            dt_start, dt_end, symbols, allocations)
        print("Start Date: ", dt_start)
        print("End Date: ", dt_end)
        print("Symbols: ", symbols)
        print("Optimal Allocations: ", allocations)
        print("Sharpe Ratio: ", sharpe)
        print("Volatility (stddev of daily returns): " , vol)
        print("Average Daily Return: ", daily_ret) 
        print("Cummulative Return: ", cum_ret)
    
    def test_example_1(self):
        dt_start = datetime(2010,1,1)
        dt_end = datetime(2010, 12, 31)
        symbols = ["APX","HPQ","IBM","HNZ"]
        allocations = [0, 0, 0, 1]
        vol, daily_ret, sharpe, cum_ret = simulate.simulate(\
            dt_start, dt_end, symbols, allocations)
        print("Start Date: ", dt_start)
        print("End Date: ", dt_end)
        print("Symbols: ", symbols)
        print("Optimal Allocations: ", allocations)
        print("Sharpe Ratio: ", sharpe)
        print("Volatility (stddev of daily returns): " , vol)
        print("Average Daily Return: ", daily_ret) 
        print("Cummulative Return: ", cum_ret)
        

    def formatTimeString(self, time):
        return datetime.strptime(time, timeFormat)
        
if __name__ == "__main__":
    unittest.main()
    


