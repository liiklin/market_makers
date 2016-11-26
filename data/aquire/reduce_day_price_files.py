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
def partition():
    oneday = 60*60*24
    indexDayTs =[]
    indexDateTs=[]
    d ={}
    ts = TimeStamp()
    for price_line in sys.stdin:
        data = price_line.split(',')
        date = ts.todate(float(data[0])/1000)
        dateTs = ts.totimestamp(date)
        price = float(data[1])
        day = datetime(date.year,date.month,date.day)
        dayTs = ts.totimestamp(day)
        if not dayTs in d:
            d[dayTs] = {}
            d[dayTs]["index"] = []
            dayTs = ts.totimestamp(day)
            indexDayTs.append(dayTs)
        if (not dateTs in d[dayTs]["index"]) and (dateTs >= dayTs) and (dateTs < dayTs + oneday):
            d[dayTs]["index"].append(dateTs)
            d[dayTs][dateTs] = price
            # print dayTs, dateTs, d[dayTs][dateTs]
    # sort the daily indexes
    for dtkey in d:
        d[dtkey]["index"] = sorted(d[dtkey]["index"])
    indexDayTs = sorted(indexDayTs)
    return (d,indexDayTs)
def process():
    current_day = end = None
    ts = TimeStamp()
    file_lines = []
    data,allDayTs = partition()
    countDay =0
    countTime =0
    # sort by day then by datetime
    for currentDayKey in allDayTs:
        countDay+=1
        currentTimeIndex = data[currentDayKey]["index"]
        if len(currentTimeIndex) > 1:
            #print "CurrentDayKey",currentDayKey, "len data",len(currentTimeIndex)

            for timeKey in currentTimeIndex:
                countTime +=1
                currentDayDate = ts.todate(currentDayKey)
                price = data[currentDayKey][timeKey]
                print "%s,%s,%s,%s,%s,%s" % (str(currentDayDate.year),str(currentDayDate.month),str(currentDayDate.day) ,str(currentDayKey),str(timeKey),str(price))
    #print "Found ", countDay, " days and ", countTime, " times"
if __name__ == "__main__":
    process()