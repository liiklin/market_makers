#!/usr/bin/env python

import sys,os,argparse
import arg_support as arg
import sys, datetime,os,json
from itertools import compress

def get_args():
    parser = argparse.ArgumentParser(description='Generate equally spaced bins from the set provided in the stdin')
    parser.add_argument('-f','--ts_file', metavar='N',required='Y', type=str, help='path to the time series json file')
    parser.add_argument('-t','--ts_name', metavar='N',required='Y', type=str, help='series name to group on')
    args = parser.parse_args()
    return args
    
def calc_bins(ts):
    ''' Calculate the bins for a list of evenly-spaced integers
    > x = [10,20,30,40,50]
    > calc_bins(x)
    [(10,19),(20,29),(30,39),(40,49),(50,59)]
    '''
    # the differnece between the first and the second item in a list
    diffItems = lambda items : items[1] - items[0]
    # the last item in a list
    lastItem = lambda items: items[-1]
    # a new list with tuples (t) where t[0] is the start of the range and t[1] is the integer just before the next range bin   
    return zip(ts, ts[1:] + [diffItems(ts) + lastItem(ts)])

def find_bin(bins,item):
    found = None
    bin_filter = map(lambda b : b[0] <= item and b[1] >= item, bins)
    matches = list(compress(bins, bin_filter))
    if len(matches) > 0:
        return matches[0]
    else :
        return None


if __name__ == '__main__':
    args = get_args()
    series = args.ts_name
    timeSeriesPath = args.ts_file
    heap_daily_avg = {}
    if os.path.exists(timeSeriesPath) and os.path.isfile(timeSeriesPath):
        with open(timeSeriesPath,'r') as fp:
            timeseries = json.load(fp)
        ts = timeseries[series]
        bins=calc_bins(ts)
        #print ranges
        for line in sys.stdin:
            # remove leading and trailing whitespace
            line = line.strip()
            # split the line into words
            words = line.split(',')

            print ','.join([str(find_bin(bins,int(words[1]))[0]),words[2],words[3],words[4],words[5],words[6],words[7],words[8]]) 

    else:
        raise FileNotFoundError(args.ts_file)