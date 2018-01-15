#!/usr/bin/env python
from __future__ import division
import sys,requests
import time
from  datetime import datetime as dtclass
from datetime import datetime, timedelta

class TimeStamp:
    def totimestamp(self,dt, epoch=datetime(1970,1,1)):
        td = dt - epoch
        # return td.total_seconds()
        return int((td.microseconds + (td.seconds + td.days * 86400) * 10**6) / 10**6) 
    def todate(self,timestamp):
        d = datetime.fromtimestamp(timestamp)
        return d
def IsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False
for line in sys.stdin:
    data = line.split(',')
    start = data[0].replace(" ","T")
    end = data[1].replace(" ","T")
    # gdax column format : [ time, low, high, open, close, volume ],
    apiurl = 'https://api.gdax.com//products/BTC-USD/candles?start=%s&end=%s&granularity=%s' % (start,end,data[2])
    ts = TimeStamp()
    startdtts = ts.totimestamp(datetime.strptime(start,'%Y-%m-%dT%H:%M:%S'))
    #print apiurl
    r = requests.get(apiurl)
    lines = {}
    for row in r.json():
        if IsInt(row[0]) and int(row[0]) >= startdtts:
            #column format : Date Time,Open,High,Low,Close,Volume,Adj Close
            lines[int(row[0])] = '%s,%s,%s,%s,%s,%s,' % (dtclass.utcfromtimestamp(int(row[0])),row[3],row[2],row[1],row[4],row[5])
    for key in sorted(lines.keys()):
        #print key, startdtts
        print lines[key]
    time.sleep(.5)

