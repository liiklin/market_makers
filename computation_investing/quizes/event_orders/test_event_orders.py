import unittest
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import time 
import logging
from event_value_below import *

class Test_Event_Orders(unittest.TestCase):
    def setUp(self):
        logging.basicConfig()
        self.logger = logging.getLogger("test")
    
    def test_find_events_vectorized(self):
        dt_start = dt.datetime(2008, 1, 1)
        dt_end = dt.datetime(2009, 12, 31)
        dt_end_2 = dt_end + dt.timedelta(days=10)
        ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))
        ldt_timestamps_2 = du.getNYSEdays(dt_start, dt_end_2, dt.timedelta(hours=16))[5:len(ldt_timestamps)+5]
        ls_data = load_data(ldt_timestamps,"sp5002008" )
        ls_symbols = ls_data["close"].columns

        self.logger.info("data loaded.")
        start = time.time()
        events = find_events_vectorized(ls_symbols, ls_data, 5)
        end = time.time()
        self.logger.info("Found events in %s" % (end - start))
        evo = create_event_orders(events, ldt_timestamps_2)
        self.logger.info("Count: %s events"  % (len(evo.index)))
    
    def test_find_events_slow(self):
        dt_start = dt.datetime(2008, 1, 1)
        dt_end = dt.datetime(2009, 12, 31)
        ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))

        ls_data = load_data(ldt_timestamps,"sp5002008" )
        ls_symbols = ls_data["close"].columns

        self.logger.info("data loaded.")
        start = time.time()
        events = find_events_vectorized(ls_symbols, ls_data, 5)
        end = time.time()
        self.logger.info("Found events in %s" % (end - start))
        evo = create_event_orders(events)
        self.logger.info("Count: %s events"  % (len(evo.index)))
        
if "__main__" in __name__:
    unittest.main()