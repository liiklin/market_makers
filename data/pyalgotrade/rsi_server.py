#!/usr/bin/python
import itertools
from pyalgotrade.optimizer import server
from pyalgotrade.barfeed import csvfeed
from pyalgotrade import bar

def parameters_generator():
    instrument = ["btc"]
    entrySMA = range(120, 170)
    exitSMA = range(8, 18)
    rsiPeriod = range(2, 4)
    overBoughtThreshold = range(90, 96)
    overSoldThreshold = range(19, 29)
    initialAmount = [5000]
    return itertools.product(instrument, entrySMA, exitSMA, rsiPeriod, overBoughtThreshold, overSoldThreshold, initialAmount)

# The if __name__ == '__main__' part is necessary if running on Windows.
if __name__ == '__main__':
	instrument = "btc"
	year = "2015"
	# Load the feed from the CSV files.
	barFeed = csvfeed.GenericBarFeed(bar.Frequency.MINUTE*30)
	barFeed.addBarsFromCSV(instrument, "30min-%s-%s.csv" % (instrument,year))
 
    #feed = yahoofeed.Feed()
	# feed.addBarsFromCSV("btc", "btc_all_daily.csv")

    # Run the server.
	server.serve(barFeed, parameters_generator(), "0.0.0.0", 5000)
