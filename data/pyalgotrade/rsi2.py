#!/usr/bin/python
from pyalgotrade import strategy
from pyalgotrade.technical import ma
from pyalgotrade.technical import rsi
from pyalgotrade.technical import cross
from pyalgotrade.bitstamp import broker

class RSI2(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, entrySMA, exitSMA, rsiPeriod, overBoughtThreshold, overSoldThreshold, amount):
        super(RSI2, self).__init__(feed)
        self.__instrument = instrument
        # We'll use adjusted close values, if available, instead of regular close values.
        if feed.barsHaveAdjClose():
            self.setUseAdjustedValues(True)
        self.__priceDS = feed[instrument].getPriceDataSeries()
        self.__entrySMA = ma.SMA(self.__priceDS, entrySMA)
        self.__exitSMA = ma.SMA(self.__priceDS, exitSMA)
        self.__rsi = rsi.RSI(self.__priceDS, rsiPeriod)
        self.__overBoughtThreshold = overBoughtThreshold
        self.__overSoldThreshold = overSoldThreshold    
        self.__longPos = None
        self.__shortPos = None
        self.getBroker().setCash(amount)

    def getEntrySMA(self):
        return self.__entrySMA

    def getExitSMA(self):
        return self.__exitSMA

    def getRSI(self):
        return self.__rsi

    def onEnterCanceled(self, position):
        if self.__longPos == position:
            self.__longPos = None
        elif self.__shortPos == position:
            self.__shortPos = None
        else:
            assert(False)
	def onEnterOk(self, position):
		execInfo = position.getEntryOrder().getExecutionInfo()
		self.info("BUY at $%.2f" % (execInfo.getPrice()))
	def onExitOk(self, position):
		if self.__longPos == position:
			self.__longPos = None
		elif self.__shortPos == position:
			self.__shortPos = None
		else:
			assert(False)
		self.info("SELL at $%.2f" % (execInfo.getPrice()))

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        position.exitMarket()

    def onBars(self, bars):
        # Wait for enough bars to be available to calculate SMA and RSI.
        if self.__exitSMA[-1] is None or self.__entrySMA[-1] is None or self.__rsi[-1] is None:
            return
        bar = bars[self.__instrument]
        signals = (self.enterLongSignal(bar), self.exitLongSignal(), self.enterShortSignal(bar), self.exitShortSignal())
        if self.__longPos is not None and self.__longPos.isOpen() and (signals[1] or signals[2]) and not self.__longPos.exitActive():
            # we are long and get a long exit signal
            print "On ?? SELL %s @ %s $%s signals : %s %s %s %s " % (self.__longPos.getShares() ,bars[self.__instrument].getPrice(), self.getBroker().getCash(), signals[0], signals[1], signals[2], signals[3])
            self.__longPos.exitMarket()
            print "Position Open: %s Age: %s Return: %s" % (self.__longPos.exitFilled(), self.__longPos.getAge(), self.__longPos.getPnL())
        elif self.__longPos is None and (signals[0] or signals[3]):
            # we are short and get a long entry signal
            shares = int(self.getBroker().getCash() * 0.9 / bars[self.__instrument].getPrice())
            print "On ?? BUY  %s @ %s $%s signals : %s %s %s %s " % (shares, bars[self.__instrument].getPrice(), self.getBroker().getCash(), signals[0], signals[1], signals[2], signals[3] )
            self.__longPos = self.enterLong(self.__instrument, shares, True)
            
    def enterLongSignal(self, bar):
        # current price is > last entrySMA and last RSI <= oversold threshold
        return bar.getPrice() > self.__entrySMA[-1] and self.__rsi[-1] <= self.__overSoldThreshold

    def exitLongSignal(self):
        # price crosses above the exitSMA and not currenlty exiting a long position
        #s = cross.cross_above(self.__priceDS, self.__exitSMA) and not self.__longPos.exitActive()
        s = cross.cross_above(self.__priceDS, self.__exitSMA) 
        if s == 0: return False
        else : return True

    def enterShortSignal(self, bar):
        # price < last entrySMA and last RSI >= overBoughtThreshold
        return bar.getPrice() < self.__entrySMA[-1] and self.__rsi[-1] >= self.__overBoughtThreshold

    def exitShortSignal(self):
        # prices crosses below exitSMA and not currently exiting short position
        #return cross.cross_below(self.__priceDS, self.__exitSMA) and not self.__shortPos.exitActive()
        s = cross.cross_below(self.__priceDS, self.__exitSMA)
        if s == 0: return False
        else : return True
 