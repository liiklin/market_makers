#!/usr/bin/python
import itertools
from pyalgotrade.optimizer import server
from pyalgotrade.barfeed import csvfeed
from pyalgotrade import bar

def parameters_generator():
    instrument = ["BTC"]
    initialCash= [1000]
    vwapWindowSize = range(90,250,5)
    buyThreshold = map(lambda x : float(x)/1000 , range(1,20,1))
    sellThreshold = map(lambda x : float(x)/1000 , range(1,20,1))
    return itertools.product(instrument, initialCash,vwapWindowSize,buyThreshold,sellThreshold)

# The if __name__ == '__main__' part is necessary if running on Windows.
if __name__ == '__main__':
    instrument = "BTC"
    year = "2016"
	# Load the feed from the CSV files.
    barFeed = csvfeed.GenericBarFeed(bar.Frequency.MINUTE*30)
    
    barFeed.addBarsFromCSV(instrument, "30min-%s-%s.csv" % (instrument,year))
  
    # Run the server.
    server.serve(barFeed, parameters_generator(), "0.0.0.0", 5001)
