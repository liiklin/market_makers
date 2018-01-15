#!/usr/bin/env python
# finds the last date in the data presented (first column from csv data)
# adds 30 minutes to it
# loops until now printing the date, date + 1 day, and 1800 (seconds in 30 minutes) 
# op all csv
import sys,datetime
from  datetime import datetime as dtclass
max_date = None
for line in sys.stdin:
    candleData = line.split(',')
    dt = dtclass.strptime(candleData[0],'%Y-%m-%d %H:%M:%S') 
   
    if max_date is None or max_date < dt:
        max_date = dt
current_date = max_date + datetime.timedelta(minutes=30)
while current_date < dtclass.utcnow():
    print "%s,%s,%s" % (current_date, current_date + datetime.timedelta(days=1),str(30 * 60))
    current_date = current_date + datetime.timedelta(days=1)