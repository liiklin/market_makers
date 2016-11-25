#!/usr/bin/env python
from __future__ import division
import sys
import datetime
from datetime import datetime, timedelta

class TimeStamp:

    def totimestamp(self,dt, epoch=datetime(1970,1,1)):
        td = dt - epoch
        # return td.total_seconds()
        return int((td.microseconds + (td.seconds + td.days * 86400) * 10**6) / 10**6) 
    def todate(self,timestamp):
        d = datetime.fromtimestamp(timestamp)
        return d

def save_to(filename,lines):
    with open(filename,"w") as fp:
        fp.writelines(lines)

def process_lines():
    current_day = end = None
    ts = TimeStamp()
    file_lines = []
    d ={}
    for price_line in sys.stdin:
        
        data = price_line.split(',')
        date = ts.todate(float(data[0])/1000)
        dateTs = ts.totimestamp(date)
        price = float(data[1])
        day = datetime(date.year,date.month,date.day)
        dayTs = ts.totimestamp(day)
        if not dayTs in d:
            d[dayTs] = {}
        if not dateTs in d[dayTs]:
            d[dayTs][dateTs] = price
    # write the results
    for currentDayKey,dayDict in d:
        for currentTimeKey,price in dayDict:
            print "%s,%s,%s" % (str(currentDayKey),str(currentTimeKey),str(price))

if __name__ == "__main__":
    process_lines()