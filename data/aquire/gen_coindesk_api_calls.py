#!/usr/bin/env python

import sys,argparse
import timestamp  
from datetime import datetime, timedelta
import numpy as np
class api_gen:
    oneday = 60*60*24
    pattern = "http://api.coindesk.com/charts/data?data=close&startdate=/sd&enddate=/ed&exchanges=bpi&dev=1&index=USD"
    start_timestamp = None
    end_timestamp = None
    rng = None
    dayCount = None
    file_count =None
    daysInRange = None
    def __init__(self,startTS,endTS,fileCount):
        self.start_timestamp = int(startTS)
        self.end_timestamp = int(endTS)
        self.rng = endTS - startTS
        self.dayCount = self.rng/self.oneday
        self.file_count = fileCount
        self.normalDaysInFile = self.dayCount/int(self.file_count) + 1
        # create a list of start/end date tuples for each day in the range
        self.daysInRange = self.get_days()
        self.daysInRange = zip(self.daysInRange,self.partition_range_bins())
    def gen_range_sets(self):
        fstart = self.start_timestamp
        dcurrent = self.start_timestamp
        
        idx = 0
        for fid in range(1,self.file_count + 1):
            fname = "api_calls_" + str(fid) + ".rng"
            # filter days in this file based on the bin setting
            set_ranges = [x[0] for x in self.daysInRange if x[1] == fid]
            api_calls = map(lambda r : self.pattern.replace('/sd',r[0].strftime('%Y-%m-%d')).replace('/ed',r[1].strftime('%Y-%m-%d')),set_ranges )
            print "Generating file ", fname

            with open(fname,'w') as fp:
                for item in api_calls:
                    fp.write(item + '\n')
                print 'Wrote ', len(api_calls),"lines."
                        
    def partition_range_bins(self):
        ts = timestamp.TimeStamp()
        daysInRange = self.get_days()
        #print daysInRange
        bins = range(self.start_timestamp,self.end_timestamp,int((self.end_timestamp-self.start_timestamp)/self.file_count))
        #print "bins", bins, "range",self.start_timestamp,self.end_timestamp
        firstItems = [ts.totimestamp(x[0]) for x in self.daysInRange]
        #print "firstItems",firstItems
        digits = np.digitize(firstItems,bins)
        digits[0]=1
        return digits

    def gen_url(self,start,end):
        ts = timestamp.TimeStamp()
        startDate = ts.todate(start)
        endDate = ts.todate(end)
        print startDate, endDate   

    def get_days(self):
        setDays = []
        TD_1DAY = timedelta(days=1)
        TD_1SECOND = timedelta(seconds=1)
        ts = timestamp.TimeStamp()
        s = ts.todate(self.start_timestamp)
        sTS = datetime(s.year, s.month, s.day)
        eTS = ts.todate(self.end_timestamp)
        currentBegin = sTS 
        currentEnd = currentBegin + TD_1DAY 
        while currentBegin < eTS:
            setDays.append((currentBegin,currentEnd))
            currentBegin = currentBegin + TD_1DAY
            currentEnd = currentBegin + TD_1DAY 
        #print "Start dt",sTS, "End dt",eTS, setDays
        return setDays
        #sTS     
def get_args():
        parser = argparse.ArgumentParser(description='Generate equally spaced bins from the set provided in the stdin')
        parser.add_argument('-c','--count_files', metavar='N',required='Y', type=str, help='number of files to create')
        parser.add_argument('-s','--start', metavar='N',required='Y', type=str, help='unix date to start on')
        parser.add_argument('-e','--end', metavar='N',required='Y', type=str, help='unix date to start on')
        args = parser.parse_args()
        return args    

if __name__ == '__main__':
    args = get_args()
    start = datetime.strptime(args.start, "%Y-%m-%d")
    end = datetime.strptime(args.end, "%Y-%m-%d")
    ts = timestamp.TimeStamp()
    a = api_gen(ts.totimestamp(start),ts.totimestamp(end),int(args.count_files))
    a.gen_range_sets()
    print args, a.rng ,a.oneday ,a.dayCount, a.normalDaysInFile
    
    
    
    
