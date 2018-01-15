#!/usr/bin/python
import sys

from datetime import datetime
for line in sys.stdin:
    candleData = line.split(',')
    if not "Date Time"  in candleData[0]:
        print datetime.strptime( candleData[0], '%Y-%m-%d %H:%M:%S') 