from pyalgotrade import bar
from pyalgotrade import strategy
from pyalgotrade import plotter
from pyalgotrade.technical import vwap
from pyalgotrade.barfeed import csvfeed
from pyalgotrade.bitstamp import broker
from pyalgotrade import broker as basebroker


class VWAPMomentum(strategy.BacktestingStrategy):
    MIN_TRADE = 5

    def __init__(self, feed, instrument,initialCash, vwapWindowSize, buyThreshold, sellThreshold):
        brk = broker.BacktestingBroker(initialCash, feed, fee=0)
        super(VWAPMomentum, self).__init__(feed, brk)
        self.__instrument = instrument
        self.__vwap = vwap.VWAP(feed[instrument], vwapWindowSize)
        self.__buyThreshold = buyThreshold
        self.__sellThreshold = sellThreshold

    def _getActiveOrders(self):
        orders = self.getBroker().getActiveOrders()
        buy = filter(lambda o: o.isBuy(), orders)
        sell = filter(lambda o: o.isSell(), orders)
        return buy, sell

    def _cancelOrders(self, orders):
        brk = self.getBroker()
        for o in orders:
            self.info("Canceling order %s" % (o.getId()))
            brk.cancelOrder(o)

    def _buySignal(self, price):
        buyOrders, sellOrders = self._getActiveOrders()
        self._cancelOrders(sellOrders)

        brk = self.getBroker()
        cashAvail = brk.getCash() * 0.98
        size = round(cashAvail / price, 3)
        if len(buyOrders) == 0 and price*size > VWAPMomentum.MIN_TRADE:
            #self.info("Buy %s at %s" % (size, price))
            try:
                self.limitOrder(self.__instrument, price, size)
            except Exception, e:
                self.error("Failed to buy: %s" % (e))

    def _sellSignal(self, price):
        buyOrders, sellOrders = self._getActiveOrders()
        self._cancelOrders(buyOrders)

        brk = self.getBroker()
        shares = brk.getShares(self.__instrument)
        if len(sellOrders) == 0 and shares > 0:
            #self.info("Sell %s at %s" % (shares, price))
            self.limitOrder(self.__instrument, price, shares*-1)

    def getVWAP(self):
        return self.__vwap

    def onBars(self, bars):
        vwap = self.__vwap[-1]
        if vwap is None:
            return

        price = bars[self.__instrument].getClose()
        if price > vwap * (1 + self.__buyThreshold):
            self._buySignal(price - .1)
        elif price < vwap * (1 - self.__sellThreshold):
            self._sellSignal(price - .1)

    def onOrderUpdated(self, order):
        if order.isBuy():
            orderType = "Buy"
        else:
            orderType = "Sell"
        displayStatus = ["FILLED"]
        if basebroker.Order.State.toString(order.getState()) in displayStatus:
            self.info("%s@%s" % (
                orderType,
                order.getExecutionInfo(),
            ))
