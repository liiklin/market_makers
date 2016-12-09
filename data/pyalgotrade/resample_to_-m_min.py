#!/usr/bin/python
from pyalgotrade.bitcoincharts import barfeed
from pyalgotrade.tools import resample
from pyalgotrade import bar
import sys,argparse
from datetime import timedelta, datetime

import datetime
# http://api.bitcoincharts.com/v1/csv/
def main(end,months,minutes=30):
	barFeed = barfeed.CSVTradeFeed()
	start = end - timedelta(months*365/12)
	print "Resampling from %s to %s" % (start,end)
	barFeed.addBarsFromCSV("/home/mcstar/data/coinbaseUSD.csv", fromDateTime=start, toDateTime=end)
	path = "./%smin-BTC-%s.csv" % (minutes,end.year)
	resample.resample_to_csv(barFeed, bar.Frequency.MINUTE*minutes, path)
	print "Saved to ",path 

def get_args():
	parser = argparse.ArgumentParser(description='Created time based candles')
	parser.add_argument('-e','--end', metavar='N',required='Y', type=str, help='End date time')
	parser.add_argument('-s','--size', metavar='N',required='Y', type=int, help='months to limit')
	parser.add_argument('-m','--minutes', metavar='N',required='N',default=30, type=int, help='Resample to -m minutes')
	args = parser.parse_args()
	return args
if __name__ == "__main__":
	args = get_args()
	end = datetime.datetime.strptime(args.end, '%Y-%m-%d')
	main(end,args.size, args.minutes)
