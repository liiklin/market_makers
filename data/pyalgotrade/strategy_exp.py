#!/usr/bin/python
from pyalgotrade import strategy
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.technical import ma

class MyStrategy(strategy.BacktestingStrategy):
	def __init__(self, feed, instrument):
		super(MyStrategy, self).__init__(feed)
		# 15 period sma over closing price 
		self.__sma = ma.SMA(feed[instrument].getCloseDataSeries(), 15)
		self.__instrument = instrument

	def onBars(self,bars):
		bar = bars[self.__instrument]
		self.info("%s %s"% (bar.getClose(), self.__sma[-1]))

#Load the feed from CSV
feed = yahoofeed.Feed()
feed.addBarsFromCSV("btc","btc_all_daily.csv")

#Evaluate the strategy with feed's bars
myStrategy = MyStrategy(feed,"btc")
myStrategy.run()
