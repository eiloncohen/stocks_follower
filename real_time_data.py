from ib_insync import *
import pandas
from datetime import datetime


class RealTimeData:
    def __init__(self):
        self.table_obj = pandas.read_csv("stocks_table.csv")
        self.ib = IB()
        self.stocks_list = self.table_obj["stock name"].tolist()

    def update_csv_table_and_close_connection(self):
        self.table_obj.to_csv("stocks_table.csv", index=False)
        self.ib.disconnect()

    def connection(self):
        self.ib.connect('127.0.0.1', 7497, clientId=1)

    def update_csv_table_with_values(self, j, stock_name, enter_price, is_down_5_percents, is_down_10_percents,
                         is_down_15_percents, is_down_20_percents, is_order_succeed):
        self.table_obj.loc[j, 'stock name'] = stock_name
        self.table_obj.loc[j, 'enter price'] = enter_price
        self.table_obj.loc[j, 'down 5% percents'] = is_down_5_percents
        self.table_obj.loc[j, 'down 10% percents'] = is_down_10_percents
        self.table_obj.loc[j, 'down 15% percents'] = is_down_15_percents
        self.table_obj.loc[j, 'down 20% percents'] = is_down_20_percents
        self.table_obj.loc[j, 'order succeed?'] = is_order_succeed

    def set_real_time_info_on_stock(self, ticker, i):
        stock = Stock(ticker, 'SMART', 'USD')
        market_data = self.ib.reqMktData(stock, "", False, False)
        self.ib.sleep(5)
        stock_name = self.table_obj.loc[i, 'stock name']
        enter_price = self.table_obj.loc[i, 'enter price']
        is_down_5_percents = self.table_obj.loc[i, 'down 5% percents']
        is_down_10_percents = self.table_obj.loc[i, 'down 10% percents']
        is_down_15_percents = self.table_obj.loc[i, 'down 15% percents']
        is_down_20_percents = self.table_obj.loc[i, 'down 20% percents']
        is_order_succeed = self.table_obj.loc[i, 'order succeed?']

        enter_price, is_down_10_percents, is_down_15_percents, is_down_20_percents, is_down_5_percents, is_order_succeed = self.update_values_for_specific_row(
            enter_price, i, is_down_10_percents, is_down_15_percents, is_down_20_percents, is_down_5_percents,
            is_order_succeed, market_data)

        print(market_data.last)
        print([stock_name, enter_price, is_down_5_percents, is_down_10_percents, is_down_15_percents, is_down_20_percents,
               is_order_succeed])
        self.update_csv_table_with_values(i, stock_name, enter_price, is_down_5_percents, is_down_10_percents,
                         is_down_15_percents, is_down_20_percents, is_order_succeed)

    def update_values_for_specific_row(self, enter_price, i, is_down_10_percents, is_down_15_percents,
                                       is_down_20_percents, is_down_5_percents, is_order_succeed, market_data):
        if pandas.isnull(enter_price):
            enter_price = market_data.last
            self.table_obj.loc[i, 'date'] = datetime.now()
        if is_order_succeed != 'yes' and is_order_succeed != 'no':
            if float(enter_price) * 0.95 >= float(market_data.last):
                is_down_5_percents = "yes"
                if float(enter_price) * 0.9 >= float(market_data.last):
                    is_down_10_percents = "yes"
                    if float(enter_price) * 0.85 >= float(market_data.last):
                        is_down_15_percents = "yes"
                        if float(enter_price) * 0.8 >= float(market_data.last):
                            is_down_20_percents = "yes"
                        else:
                            is_down_20_percents = "no"
                    else:
                        is_down_15_percents = "no"
                        is_down_20_percents = "no"
                else:
                    is_down_10_percents = "no"
                    is_down_15_percents = "no"
                    is_down_20_percents = "no"
            else:
                is_down_5_percents = "no"
                is_down_10_percents = "no"
                is_down_15_percents = "no"
                is_down_20_percents = "no"
        if pandas.isnull(is_order_succeed):
            if float(enter_price) * 1.1 <= float(market_data.last):
                is_order_succeed = "no"
            if float(enter_price) * 0.9 >= float(market_data.last):
                is_order_succeed = "yes"
        return enter_price, is_down_10_percents, is_down_15_percents, is_down_20_percents, is_down_5_percents, is_order_succeed

