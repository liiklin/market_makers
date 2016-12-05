#!/usr/bin/python
from pyalgotrade import strategy
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.technical import ma

class MyStrategy(strategy.BacktestingStrategy):
	def __init__(self, feed, instrument, smaPeriod):
		super(MyStrategy, self).__init__(feed,10000)
		self.__position=None
		self.__instrument = instrument
		self.__value = 0
		#self.setUseAdjustedValues(True)
		self.__sma = ma.SMA(feed[instrument].getPriceDataSeries(), smaPeriod)

	def onEnterOk(self,position):
		#print position
		execInfo = position.getEntryOrder().getExecutionInfo()
		self.info("BUY at $%.2f, portfolio :$%.2f" % (execInfo.getPrice(),self.getResult() ))
	
	def onEnterCanceled(self, position):
		self.__position = None

	def onExitOk(self,position):
		execInfo = position.getExitOrder().getExecutionInfo()
		self.__value = self.getResult()
		self.info("Sell at $%.2f, portfolio :$%.2f" % (execInfo.getPrice(),self.getResult()))
		self.__position = None
	def onExecitCanceled(self, position):
		#if the exit was canceled, re-submit it.
		self.__position.exitMarket()
	def onBars(self,bars):
		# wait for enough bars to be available to calculate SMA.
		if self.__sma[-1] is None :
			return
		bar = bars[self.__instrument]
		# If a position was not opened, check if we should enter a long position.
		if self.__position is None:
			if bar.getPrice() > self.__sma[-1]:
				ordersize = 10
				if self.__value > 0:
					ordersize=self.__value/bar.getPrice()
				#	print ordersize, self.__value, bar.getPrice()
				# Enter a buy market order for 10 shares.  The order is good till canceled.
				self.__position = self.enterLong(self.__instrument,ordersize,True)
		elif bar.getPrice() < self.__sma[-1] and not self.__position.exitActive():
			self.__position.exitMarket()

def run_strategy(smaPeriod):
	#Load the feed from CSV
	feed = yahoofeed.Feed()
	feed.addBarsFromCSV("btc","btc_all_daily.csv")

	#Evaluate the strategy with feed's bars
	myStrategy = MyStrategy(feed,"btc", smaPeriod)
	myStrategy.run()
	print "Final portfolio value: $%.2f" % myStrategy.getBroker().getEquity()

for x in range(5,10):
	print "SMA Period", x
	run_strategy(x)
