#!/usr/bin/env python
import unittest
from  gen_coindesk_api_calls import api_gen
from timestamp import TimeStamp
from datetime import datetime, timedelta
import numpy as np
class TestGenCoindesk(unittest.TestCase):
    
    def test_get_days_correct_len(self):
        ts = TimeStamp()
        startTS = ts.totimestamp(datetime.today()  - timedelta(days=9))
        endTS = ts.totimestamp(datetime.today())
        a = api_gen(startTS,endTS,10)
        self.assertTrue(len(a.daysInRange) == 10,"Should be 10 days got " + str(len(a.daysInRange)))

    def test_get_days_rolls_to_midnight(self):
        ts = TimeStamp()
        startTS = ts.totimestamp(datetime.today() - timedelta(days=2))
        endTS = ts.totimestamp(datetime.today())
        sdt = ts.todate(startTS)
        shouldStartAm = datetime(sdt.year,sdt.month,sdt.day)
        a = api_gen(startTS,endTS,100)
        self.assertTrue(a.daysInRange[0][0][0] == shouldStartAm,"first date incorrect expected:" + str(shouldStartAm) + " got :" + str(a.daysInRange[0][0][0]) )

    def test_partition_range_bins(self):
        ts = TimeStamp()
        startTS = ts.totimestamp(datetime.today() - timedelta(days=200))
        endTS = ts.totimestamp(datetime.today())
        a = api_gen(startTS,endTS,10)
        bins = [x[1] for x in a.daysInRange]
        self.assertTrue(max(bins) == 10)
        self.assertTrue(min(bins) == 1)
        
        


if __name__ == '__main__':
    unittest.main()
