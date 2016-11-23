#!/usr/bin/env python

import sys
import datetime
from  timestamp import TimeStamp
from datetime import datetime, timedelta

def save_to(filename,lines):
    with open(filename,"w") as fp:
        fp.writelines(lines)

def process_lines():
    current_day = end = None
    ts = TimeStamp()
    file_lines = []

    for price_line in sys.stdin:
        
        data = price_line.split(',')
        date = ts.todate(float(data[0])/1000)
        price = float(data[1])
        if not current_day:
            current_day = datetime(date.year,date.month,date.day)
            end = current_day + timedelta(days=1)  
        else:
            if date >= end:
                if len(file_lines) > 10:
                    save_to("%s.csv" % str(ts.totimestamp(current_day)),file_lines) 
                file_lines=[]           
                # set the next file date
                current_day = datetime(date.year,date.month,date.day) 
                end = current_day + timedelta(days=1)
        file_lines.append("%s,%s" % (str(ts.totimestamp(date)),str(price)))
    if len(file_lines) > 10:
        save_to("%s.csv" % str(ts.totimestamp(current_day)),file_lines)

if __name__ == "__main__":
    process_lines()