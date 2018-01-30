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
    def formatTimeString(self, time):
        return datetime.strptime(time, timeFormat)
        
if __name__ == "__main__":
    unittest.main()
    

