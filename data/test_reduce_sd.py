#!/usr/bin/env python
import unittest
import reduce_sd as rsd
import collections
import numpy as np
class TestReduceSd(unittest.TestCase):
    def test_init_creates_columns(self):
        cols = ["a","b"]
        r = rsd.reduce(cols)
        self.assertIsNotNone(r.columns)
        self.assertTrue(r.columns == cols)
    def test_init_creates_sdList(self):
        cols = ["a","b"]
        r = rsd.reduce(cols)
        self.assertIsNotNone(r.sdList)
    def test_add_row_no_key_creates_entry(self):
        r = rsd.reduce(["a","b","c"])
        r.add_row([1,2,3,4],999999)
        self.assertIsNotNone(r.sdList[999999])    



if __name__ == '__main__':
    unittest.main()