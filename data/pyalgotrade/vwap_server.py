#!/usr/bin/python
import itertools
from pyalgotrade.optimizer import server
from pyalgotrade.barfeed import csvfeed
from pyalgotrade import bar
lenparams = 0
def parameters_generator():
    instrument = ["BTC"]
    initialCash= [1000]
    vwapWindowSize = range(89,180,1)
    buyThreshold = map(lambda x : float(x)/1000 , range(5,40,1))
    sellThreshold = map(lambda x : float(x)/1000 , range(5,40,1))
    lenparams = len(sellThreshold) * len(buyThreshold) * len(vwapWindowSize)
    return (lenparams, itertools.product(instrument, initialCash,vwapWindowSize,buyThreshold,sellThreshold))

# The if __name__ == '__main__' part is necessary if running on Windows.
if __name__ == '__main__':
    instrument = "BTC"
    year = "2016"
    minutes = 30
    
	# Load the feed from the CSV files.
    barFeed = csvfeed.GenericBarFeed(bar.Frequency.MINUTE*30)
    
    barFeed.addBarsFromCSV(instrument, "%smin-%s-%s.csv" % (minutes,instrument,year))
  
    # Run the server.
    lenp, params = parameters_generator()
    print "Running %s variations" % lenp
    server.serve(barFeed,params, "0.0.0.0", 5001)
