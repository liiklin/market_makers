#!/usr/bin/env python
from datetime import datetime, timedelta
import sys,argparse

class TimeStamp:
    
    def totimestamp(self,dt, epoch=datetime(1970,1,1)):
        td = dt - epoch
        # return td.total_seconds()
        return int((td.microseconds + (td.seconds + td.days * 86400) * 10**6) / 10**6) 
    def todate(self,timestamp):
        d = datetime.fromtimestamp(timestamp)
        return d

class candles:
    current_set = []
    ts = None
    minutes = 0
    def __init__(self, minutes=5, hours=0):
        self.minutes = hours * 60 + minutes
        self.ts = TimeStamp()
    def high(self):
        return max([x[2] for x in self.current_set])
    def low(self):
        return min([x[2] for x in self.current_set])
    def open(self):
        return self.current_set[0][2]
    def close(self):
        return self.current_set[len(self.current_set)-1][2]
    def adjclose(self):
        return self.close()
    def volume(self):
        return 100
    def date(self):
        return self.current_set[len(self.current_set)-1][1]
    def min_date(self):
        return min([x[1] for x in self.current_set])
    
        
    def parse(self,line):
        data = price_line.split(',')
        if not data[0] == "Date":
            parsed = (self.ts.todate(int(data[3])),self.ts.todate(int(data[4])),float(data[5]))
            self.current_set.append(parsed)
            td = parsed[1] - self.min_date()
            #print str(self.minutes), str(td.total_seconds()/60), parsed[1], self.min_date(),  parsed[1] -  self.min_date(), len(self.current_set)
            if self.minutes < td.total_seconds()/60:
                print ",".join([self.date().strftime("%Y-%m-%d 00:00"), str(self.open()),str(self.high()),str(self.low()),str(self.close()),str(self.volume()),str(self.adjclose())])
                self.current_set[:]=[] 
            

def get_args():
    parser = argparse.ArgumentParser(description='Created time based candles')
    parser.add_argument('-m','--minutes', metavar='N',required='N', type=int, help='Number of minutes for each candle, defaults to 5')
    parser.add_argument('-H','--hours', metavar='N',required='N', type=int, help='Number of hours for each candle, defaults to 0')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = get_args()
    c= None
    if (args.minutes and args.minutes > 0) or (args.hours and args.hours > 0) :
        c = candles(max([args.minutes,0]),max([args.hours,0]))
    else:
        c = candles()
	print "Date Time,Open,High,Low,Close,Volume,Adj Close"
    for price_line in sys.stdin:
        c.parse(price_line)
        
