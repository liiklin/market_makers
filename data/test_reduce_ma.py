import unittest
import reduce_ma
import collections
import numpy as np
class TestReduceMa(unittest.TestCase):
    
    def test_build_col_vals_ignore_id(self):
        r = reduce_ma.reduce(["a","b","c"])
        tup_set = r.build_col_values(["1","2","3","4"])
        self.assertTrue(len(tup_set.keys()) == 3,"Should have same number of items as the column list")
        tsvals = map(lambda item : tup_set[item],tup_set.keys())
        filterOnes = np.array(tsvals) == 1
        #print tsvals
        self.assertTrue(not any(filterOnes),"The id column should not be included")

    def test_build_col_vals_all_floats(self):
        r = reduce_ma.reduce(["a","b","c"])
        obj_set = r.build_col_values(["1","2","3","4"])
        numbers = map(lambda t : obj_set[t], sorted(obj_set.keys()) )
        #print numbers
        correct = [2.0,3.0,4.0]
        self.assertTrue(numbers == correct, "values should be converted to float")
        
    def test_cumsum_nokey_createnew(self):
        r = reduce_ma.reduce(["a","b","c"])
        #print "66 in cumsum" ,r.cumSum
        r.add_cumSum({"a":2,"b":3,"c":4},66)
        self.assertTrue(66 in r.cumSum,"add_cumSum should create a new key if it does not exist")

    def test_cumsum_keyexists_addvalues(self):
        r = reduce_ma.reduce(["a","b","c"])
        r.cumSum[66] = {"a":1,"b":1,"c":2,"count":0}
        r.add_cumSum({"a":2.0,"b":3.0,"c":4.0},66)
        self.assertTrue(66 in r.cumSum,"add_cumSum should create a new key if it does not exist")
    def test_cumsum_add_increments_count(self):
        r = reduce_ma.reduce(["a","b","c"])
        r.cumSum[66] = {"a":1,"b":1,"c":2,"count":0}
        self.assertTrue(r.cumSum[66]["count"] == 0,"test value should start at zero")
        r.add_cumSum({"a":2.0,"b":3.0,"c":4.0},66)
        self.assertTrue(r.cumSum[66]['count'] == 1,"count should be incremented")
    def test_compute_ma_clears_cnt(self):
        r = reduce_ma.reduce(["a","b","c"])
        r.cumSum[1] = {"a":100,"b":200,"c":300,"count":10}
        r.compute_ma()
        print r.ma
        self.assertTrue("count" not in r.ma[1],"Should remove count when compute is complete")
        
if __name__ == '__main__':
    unittest.main()
