#!/usr/bin/env python
from datetime import datetime, timedelta
import sys

class TimeStamp:
    
    def totimestamp(self,dt, epoch=datetime(1970,1,1)):
        td = dt - epoch
        # return td.total_seconds()
        return int((td.microseconds + (td.seconds + td.days * 86400) * 10**6) / 10**6) 
    def todate(self,timestamp):
        d = datetime.fromtimestamp(timestamp)
        return d

class five_min_candles:
    current_set = []
    ts = None
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
        return -1
    def date(self):
        return self.current_set[len(self.current_set)-1][1]
    def __init__(self):
        self.ts = TimeStamp()
    def parse(self,line):
        data = price_line.split(',')
        parsed = (self.ts.todate(int(data[3])),self.ts.todate(int(data[4])),float(data[5]))
        self.current_set.append(parsed)
        if len(self.current_set) % 5 == 0:
            print ",".join([self.date().strftime("%Y-%m-%dT%H:%M"), str(self.open()),str(self.high()),str(self.low()),str(self.close()),str(self.volume()),str(self.adjclose())])
            self.current_set=[] 
            


if __name__ == "__main__":
    c = five_min_candles()

    for price_line in sys.stdin:
        c.parse(price_line)
        
