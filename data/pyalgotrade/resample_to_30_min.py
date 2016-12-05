#!/usr/bin/python
from pyalgotrade.bitcoincharts import barfeed
from pyalgotrade.tools import resample
from pyalgotrade import bar

import datetime
# http://api.bitcoincharts.com/v1/csv/
def main():
	barFeed = barfeed.CSVTradeFeed()
	barFeed.addBarsFromCSV("/home/mcstar/data/.coinbaseUSD.csv", fromDateTime=datetime.datetime(2015, 1, 1), toDateTime=datetime.datetime(2015,12,31))
	resample.resample_to_csv(barFeed, bar.Frequency.MINUTE*30, "./30min-btc-2015.csv")


if __name__ == "__main__":
	main()
