#!/usr/bin/env python

import sys,argparse
import timestamp

class api_gen:
    pattern = "http://api.coindesk.com/charts/data?data=close&startdate=/sd&enddate=/ed&exchanges=bpi&dev=1&index=USD"
    def get_args(self):
        parser = argparse.ArgumentParser(description='Generate equally spaced bins from the set provided in the stdin')
        parser.add_argument('-c','--count_files', metavar='N',required='Y', type=str, help='number of files to create')
        parser.add_argument('-s','--start', metavar='N',required='Y', type=str, help='unix date to start on')
        parser.add_argument('-e','--end', metavar='N',required='Y', type=str, help='unix date to start on')
        args = parser.parse_args()
        return args
    def gen_url(self,start,end):
        ts = timestamp.TimeStamp()
        startDate = ts.todate(start)
        endDate= = ts.todate(end)
        print startDate, endDate        
    
if __name__ == '__main__':
    args = get_args()
    start = int(args.start)
    end = int(args.end)
    rng = end - start 
    oneday = 60*60*24
    days = rng/oneday
    fileCount = int(args.count_files)
    normalDaysInFile = days/int(args.count_files) + 1
    fstart = start
    dcurrent = start
    for x in range(fileCount):
        
        fname = "api_calls" + str(x) + ".rng"
        with open(fname,'w') as fp:
            while fstart + dcurrent <      

    print args, rng,oneday,days,normalDaysInFile
    
