from stock import StockInfo
from interactive_info import InteractiveInfo


# connect to interactive
ib = InteractiveInfo()
ib.connect()

# create stock and get historical info from interactive brokers
dkng = StockInfo('DLO')
dkng.history_info_on_stock = ib.get_history_data_on_stock(dkng.stock)

# check
dkng.check_bullish_engulfing_pattern()


ib.disconnect()
