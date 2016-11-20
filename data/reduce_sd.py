#!/usr/bin/env python
import numpy as np
import sys,os,argparse

def get_args():
    parser = argparse.ArgumentParser(description='Generate equally spaced bins from the set provided in the stdin')
    parser.add_argument('-m','--map', metavar='N', type=str, help='map of values to extract as a comma seperated list of column names')
    args = parser.parse_args()
    return args

class reduce:
    sdList = None
    columns = None
    ma = {}
    currentSet =None
    currentKey = None
    def __init__(self,columns):
        self.columns = columns
        self.sdList = {}

    def build_col_values(self,words):
        # ["1","10","20","30"]  => [10.0,20.0,30.0] 
        vals = map( lambda s : float(s), words[1:len(self.columns)+1] )
        # [10.0,20.0,30.0] => [("Col1",10.0),("Col2",20.0),("Col3",30.0)]
        colvals = zip( self.columns, vals )
        # [("Col1",10.0),("Col2",20.0),("Col3",30.0)] => {"Col1":10.0,"Col2":20.0,"Col3":30.0}
        return dict(colvals)

    def add_row(self,row,key):
        #if key dne, and key not equal current key,
        if key not in self.sdList:
            self.sdList[key] = row 
        # compute_sd of last key
        # store 
        # if key DNE create new
        print ''
         
        

    def compute_sd(self):
        self.ma = {}
        for item in self.cumSum:
            cnt = self.cumSum[item]["count"]
            #mean = diect(map(lambda k : ))
            computed = dict(map(lambda k : (k, self.cumSum[item][k]/cnt), self.cumSum[item].keys()))
            computed.pop("count",None)
            self.ma[item] = computed
            
    def init_current(self,key,set_vals):
        self.currentSet = []
        self.currentKey = key

    def parse_input(self):
        # input comes from STDIN
        for line in sys.stdin:
            line = line.strip()
            # split the line into words
            words = line.split(',')
            line_vals = self.build_col_values( words )
            # print "line, words", line_vals, words
            self.add_cumSum(line_vals,int(words[0]))
        self.compute_ma()
        print self.ma

if __name__ == '__main__':
    r = reduce(["open","high","low","close","volume","trades"])
    r.parse_input()