#!/usr/bin/python
from pyalgotrade import strategy
from pyalgotrade.barfeed import yahoofeed


class MyStrategy(strategy.BacktestingStrategy):
	def __init__(self, feed, instrument):
		super(MyStrategy, self).__init__(feed)
		self.__instrument = instrument

	def onBars(self,bars):
		bar = bars[self.__instrument]
		self.info(bar.getClose())

#Load the feed from CSV
feed = yahoofeed.Feed()
feed.addBarsFromCSV("btc","btc_all_daily.csv")

#Evaluate the strategy with feed's bars
myStrategy = MyStrategy(feed,"btc")
myStrategy.run()
