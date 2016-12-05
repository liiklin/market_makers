#!/usr/bin/python
from pyalgotrade import strategy
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.technical import ma
from pyalgotrade.technical import rsi

class MyStrategy(strategy.BacktestingStrategy):
	def __init__(self, feed, instrument):
		super(MyStrategy, self).__init__(feed)
		self.__rsi = rsi.RSI(feed[instrument].getCloseDataSeries(), 14)
		# 5 period sma over closing price 
		self.__sma5 = ma.SMA(self.__rsi, 5)
		# 15 period sma over closing price 
		self.__sma15 = ma.SMA(self.__rsi, 15)
		self.__instrument = instrument

	def onBars(self,bars):
		bar = bars[self.__instrument]
		self.info("%s %s %s %s"% (bar.getClose(),self.__rsi[-1], self.__sma5[-1],self.__sma15[-1]))

#Load the feed from CSV
feed = yahoofeed.Feed()
feed.addBarsFromCSV("btc","btc_all_daily.csv")

#Evaluate the strategy with feed's bars
myStrategy = MyStrategy(feed,"btc")
myStrategy.run()
