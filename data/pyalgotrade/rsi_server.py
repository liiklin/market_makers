#!/usr/bin/python
import itertools
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.optimizer import server


def parameters_generator():
    instrument = ["btc"]
    entrySMA = range(99, 15)
    exitSMA = range(8, 16)
    rsiPeriod = range(2, 4)
    overBoughtThreshold = range(75, 96)
    overSoldThreshold = range(16, 26)
    return itertools.product(instrument, entrySMA, exitSMA, rsiPeriod, overBoughtThreshold, overSoldThreshold)

# The if __name__ == '__main__' part is necessary if running on Windows.
if __name__ == '__main__':
    # Load the feed from the CSV files.
    feed = yahoofeed.Feed()
    feed.addBarsFromCSV("btc", "btc_all_5_min.csv")

    # Run the server.
    server.serve(feed, parameters_generator(), "localhost", 5000)
