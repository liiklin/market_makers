#!/usr/bin/env python

from operator import itemgetter
import sys, datetime,os,json
import time

min_dt = sys.maxsize
max_dt = 0

def dt(u): return datetime.datetime.fromtimestamp(u)
def ts(u): return int(time.mktime(u.timetuple()))
def get_args():
    parser = argparse.ArgumentParser(description='Generate equally spaced bins from the set provided in the stdin')
    parser.add_argument('-d','--dest', metavar='N', type=str, help='path to save the result')
    args = parser.parse_args()
    return args

def save_to(obj,path):
    if os.path.isfile(path):
        os.remove(path)
    with open(path,'w') as fp:
        json.dump(obj,fp)

args = get_args()

# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = int(line.strip())
    min_dt = min([line,min_dt])
    max_dt = max([line,max_dt]) 

x = dt(min_dt)
start = ts(datetime.datetime(x.year,x.month,x.day,0,0))
print '%s\t%s' % (dt(start), dt(max_dt))
step24hr = 24 * 60 * 60
step1hr = 60 * 60 
step10min = 60 * 10
twentyFourHour = range(start,max_dt,step24hr)
hours = range(start,max_dt,step1hr)
tenMin = range(start,max_dt,step10min) 

data =  {'Days':twentyFourHour,"Hours":hours,"TenMin":tenMin}
if args.dest and len(args.dest) > 0:
    print args.dest
    with open('./' + args.dest,'w') as fp:
        json.dump(data,fp)
        print "Wrote",args.dest