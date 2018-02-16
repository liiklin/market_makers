import unittest
from datetime import datetime
from market_sim import *
import os

class Test_Market_Sim(unittest.TestCase):
    #def setUp(self):
        #os.environ['QSDATA']= '/home/mcstar/QSTK-0.2.8/QSTK/QSData/'
        #os.environ['QSSCRATCH'] = '/home/mcstar/QSTK-0.2.8/QSTK/QSData/Scratch'
        #os.environ["SYMBOLS"] = "sp5002008.txt"
        
    def test_process_order(self):
        # arrange
        
        orders = [{"symbol":"GOOG", "date":datetime(2008,1,1), \
        "action":"BUY","shares":199}, 
        {"symbol":"AAPL", "date":datetime(2008,12,31), \
        "action":"BUY","shares":299}]
        # act
        result = process_orders(orders)
        # assert
        self.assertIsNotNone(result)

if __name__ == "__main__":
    unittest.main()