from ib_insync import *

DURATION = '120 D'
BATSIZESETTING = '1 day'

class InteractiveInfo:
    def __init__(self):
        self.ib = IB()

    def connect(self):
        self.ib.connect('127.0.0.1', 7497, clientId=1)

    def disconnect(self):
        self.ib.disconnect()

    def get_history_data_on_stock(self, stock):
        bars = self.ib.reqHistoricalData(stock, endDateTime='', durationStr=DURATION,
                                    barSizeSetting=BATSIZESETTING, whatToShow='TRADES', useRTH=True)
        df = util.df(bars)
        return df