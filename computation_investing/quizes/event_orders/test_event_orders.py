import sys, os
MY_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, MY_PATH + '/../')
import unittest
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import time 
import logging
from event_value_below import *

class Test_Event_Orders(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger("test")
        logging.basicConfig()
    
    def test_offset_timestamps(self):
        dt_start = dt.datetime(2008, 1, 1)
        dt_end = dt.datetime(2009, 12, 31)
        evo = EventOrders("sp5002008",dt_start, dt_end)
        dt_lookups = [dt.datetime(2008,1,7,16), dt.datetime(2009,1,10,16)]
        offsets = evo.get_offset_timestamps(dt_lookups) 
        expected_days = [dt.datetime(2008,1,14,16), \
            dt.datetime(2009,1,16,16)]
        results = offsets.isin(expected_days)
        self.assertTrue(all(results), "expected dates missing")
        
    def test_find_events_vectorized(self):
        
        dt_start = dt.datetime(2008, 1, 1)
        dt_end = dt.datetime(2009, 12, 31)
        evo = EventOrders("sp5002008", dt_start, dt_end)
        
        self.logger.info("data loaded.")
        start = time.time()
        events = evo.find_events_vectorized(5)
        
        end = time.time()
        self.logger.info("Found events in %s" % (end - start))
        ldt_sell = evo.get_offset_timestamps(events.index, days_offset=5)
        self.assertTrue(ldt_sell.shape == events.index.shape, "Should have the same number of sells as buys")
        orders = evo.create_event_orders(events, ldt_sell)
        self.logger.info("Count: %s events"  % (len(orders.index)))
        self.logger.info(orders.to_csv())
    
    def test_event_simulate(self):
        dt_start = dt.datetime(2008, 1, 1)
        dt_end = dt.datetime(2009, 12, 31)
        evo = EventOrders("sp5002008", dt_start, dt_end)

        self.logger.info("data loaded.")
        start = time.time()
        events = evo.find_events_vectorized(5)
        
        end = time.time()
        self.logger.info("Found events in %s" % (end - start))
        ldt_sell = evo.get_offset_timestamps(events.index, days_offset=5)
        self.assertTrue(ldt_sell.shape == events.index.shape, "Should have the same number of sells as buys")
        orders = evo.create_event_orders(events, ldt_sell)
        self.logger.info("Count: %s events"  % (len(orders.index)))
        evo.simulate(orders)

    def test_orders_2_sample_analyze(self):
        file_name = "computational_investing/quizes/event_orders/orders2.csv"
        orders = pd.read_csv(file_name,header="infer")
        dt_start = dt.datetime(2011,1,14)
        dt_end = dt.datetime(2011,12,14)
        portfolio, evo = self.produce_portfolio(orders, dt_start, dt_end)

    def produce_portfolio(self, orders, dt_start, dt_end):
        orders.columns = ["year", "month", "day", "symbol", "action","amount"]
        symbols = pd.DataFrame(orders["symbol"].unique(), columns=["symbol"])
        ls_symbol = [y for x  in symbols.values for y in x]
        evo = EventOrders(ls_symbol, dt_start, dt_end)
        orders.index = evo.generate_order_dates(orders) + dt.timedelta(hours=16)
        #print orders.index
        #display_side_by_side(orders,symbols)
        results = evo.simulate(orders,cash=1000000)
        #display_side_by_side(results.head(), results.tail())
        return results, evo
    
    #def test_find_events_slow(self):
    #    dt_start = dt.datetime(2008, 1, 1)
    #    dt_end = dt.datetime(2009, 12, 31)
    #    evo = EventOrders(dt_start, dt_end)
    #    #ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))
    #    
    #    ldt_timestamps_2 = evo.get_offset_timestamps(events.index, days_offset=5)
#
    #    ls_data = evo.load_data("sp5002008")
    #    ls_symbols = ls_data["close"].columns
#
    #    self.logger.info("data loaded.")
    #    start = time.time()
    #    events = evo.find_events_vectorized(ls_symbols, ls_data, 5)
    #    end = time.time()
    #    self.logger.info("Found events in %s" % (end - start))
    #    orders = evo.create_event_orders(events, ldt_timestamps_2)
    #    self.logger.info("Count: %s events"  % (len(orders.index)))
        
if "__main__" in __name__:
    unittest.main()