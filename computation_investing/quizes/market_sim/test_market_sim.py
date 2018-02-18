import unittest
from datetime import datetime
from simulate import process_orders
import os

class Test_Market_Sim(unittest.TestCase):
    #def setUp(self):
        #os.environ['QSDATA']= '/home/mcstar/QSTK-0.2.8/QSTK/QSData/'
        #os.environ['QSSCRATCH'] = '/home/mcstar/QSTK-0.2.8/QSTK/QSData/Scratch'
        #os.environ["SYMBOLS"] = "sp5002008.txt"
        
    def test_process_order(self):
        # arrange
        order_dates=[datetime(2008,1,1),datetime(2008,1,2), datetime(2008,3,1), datetime(2008,5,3)]
        orders = {"date":order_dates,"GOOG":[10,10,2,0], "AAPL":[0,0,0,20], "XOM":[50,50,32,0]}
        #orders = [{"symbol":"GOOG", "date":datetime(2008,1,1), \
        #"action":"BUY","shares":199}, 
        #{"symbol":"XOM", "date":datetime(2008,3,1), \
        #"action":"BUY","shares":299}]
        # act
        result = process_orders(orders)
        # assert
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()