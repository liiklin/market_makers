#!/usr/bin/env python
# finds the last date in the data presented (first column from csv data)
# adds 30 minutes to it
# loops until now printing the date, date + 1 day, and 1800 (seconds in 30 minutes) 
# op all csv
import sys,datetime
from  datetime import datetime as dtclass
earliest_date = dtclass.utcnow() - datetime.timedelta(days=90)
#print earliest_date
print "Date Time,Open,High,Low,Close,Volume,Adj Close"
for line in sys.stdin:
    candleData = line.split(',')
    if "Date" not in candleData[0]:
        dt = dtclass.strptime(candleData[0],'%Y-%m-%d %H:%M:%S')    
        if dt >= earliest_date:
            #print dt, earliest_date , dt >= earliest_date
            print line.replace("\n",'') 
 
