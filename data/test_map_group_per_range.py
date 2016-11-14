import unittest
import map_group_per_range
class TestMapGroup(unittest.TestCase):
    def test_calc_ranges_includes_ends(self):
        start = 100
        end = 201 
        ts = range(start,end,10)
        #print ts
        tr = map_group_per_range.calc_bins(ts)
        inc_s = False
        inc_e = False
        for x in tr:
            if start >= x[0] and start <= x[1]:
                inc_s = True
            if end >=x[0] and end <=x[1]:
                inc_e = True
        self.assertTrue(inc_s,"The starting range was not found. (" + str(start) + ")")
        self.assertTrue(inc_e,"The ending range was not found. (" + str(end) + ")")
        #print tr
    def test_calc_bins_count(self):
        start = 100
        end = 200
        ts = range(start,end,10)
        tr = map_group_per_range.calc_bins(ts)
        self.assertTrue(len(tr) ==len(ts),"len calc_bins  wrong actual:" + str(len(tr)) + " expected:10" )

    def test_calc_bins_includes_all(self):
        start = 100
        end = 200
        
        binIncludes = lambda bins,item : map(lambda x : x[0] <= item and x[1] >= item,bins)
        ts = range(start,end,10)
        tb = map_group_per_range.calc_bins(ts)
        
        result =all(map( lambda t : any(binIncludes(tb,t)),ts))
        #print result
        self.assertTrue(result ,"One or more items not found in bins")
                
    def test_find_bin_no_match_none(self):
        tb =[(100,109),(120,129),(130,139),(140,149),(150,159)]
        result = map_group_per_range.find_bin(tb,1)
        self.assertTrue(not result,"Should be none for out of range.")
    def test_find_bin_match_first_item(self):
        tb =[(100,109),(120,129),(130,139),(140,149),(150,159)]
        result = map_group_per_range.find_bin(tb,100)
        self.assertTrue( result,"Should not be none for item in range.")
        self.assertTrue(result[0] == 100 and result[1] == 109, "Should find first bin.")
    def test_find_bin_match_last(self):
        tb =[(100,109),(120,129),(130,139),(140,149),(150,159)]
        result = map_group_per_range.find_bin(tb,151)
        self.assertTrue( result,"Should not be none for item in range.")
        self.assertTrue(result[0] == 150 and result[1] == 159, "Should find last bin.")
    def test_find_bin_outside_none(self):
        tb =[(100,109),(120,129),(130,139),(140,149),(150,159)]
        result = map_group_per_range.find_bin(tb,60)
        self.assertTrue(not result,"None result expected for values outside the bin range")
        result = map_group_per_range.find_bin(tb,600)
        self.assertTrue(not result,"None result expected for values outside the bin range")


if __name__ == '__main__':
    unittest.main()
        
