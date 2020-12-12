from __future__ import (absolute_import, division, print_function,
                        unicode_literals)


 #In Progress
import backtrader as bt


class St(bt.Strategy):
    def __init__(self):
        self.sma = bt.indicators.SimpleMovingAverage(self.data)


data = bt.feeds.BacktraderCSVData(dataname='../../datas/2005-2006-day-001.txt')

cerebro = bt.Cerebro()
cerebro.adddata(data)
cerebro.addstrategy(St)
cerebro.run()
cerebro.plot()