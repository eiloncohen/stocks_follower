import express as express
from ib_insync import *
import pandas
import prettytable
import streamlit as st
import plotly.express as px

# read data from stocks file and enter it to list
table_obj = pandas.read_csv("stocks_table.csv")
stocks_list = table_obj["stock name"].tolist()


# connect to interactive brokers
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)


def update_csv_table(stocks_table, j, stock_name, enter_price, is_down_5_percents, is_down_10_percents, is_down_15_percents, is_down_20_percents, is_order_succeed):
    stocks_table.loc[j, 'stock name'] = stock_name
    stocks_table.loc[j, 'enter price'] = enter_price
    stocks_table.loc[j, 'down 5% percents'] = is_down_5_percents
    stocks_table.loc[j, 'down 10% percents'] = is_down_10_percents
    stocks_table.loc[j, 'down 15% percents'] = is_down_15_percents
    stocks_table.loc[j, 'down 20% percents'] = is_down_20_percents
    stocks_table.loc[j, 'order succeed?'] = is_order_succeed


def get_real_time_info_on_stock(ticker, i):
    stock = Stock(ticker, 'SMART', 'USD')
    market_data = ib.reqMktData(stock, "", False, False)
    ib.sleep(5)
    stock_name = table_obj.loc[i, 'stock name']
    enter_price = table_obj.loc[i, 'enter price']
    is_down_5_percents = table_obj.loc[i, 'down 5% percents']
    is_down_10_percents = table_obj.loc[i, 'down 10% percents']
    is_down_15_percents = table_obj.loc[i, 'down 15% percents']
    is_down_20_percents = table_obj.loc[i, 'down 20% percents']
    is_order_succeed = table_obj.loc[i, 'order succeed?']

    if pandas.isnull(enter_price):
        enter_price = market_data.last

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

    print(market_data.last)
    print([stock_name,enter_price,is_down_5_percents,is_down_10_percents,is_down_15_percents, is_down_20_percents,is_order_succeed])
    update_csv_table(table_obj, i, stock_name, enter_price, is_down_5_percents, is_down_10_percents, is_down_15_percents, is_down_20_percents, is_order_succeed)

# for i, stock in enumerate(stocks_list):
#     get_real_time_info_on_stock(stock, i)


#create the result of table
# table_obj.to_csv("stocks_table.csv")

stocks_table_csv = pandas.read_csv("stocks_table.csv")
st.set_page_config(page_title = "Shagim followers stocks")
print(stocks_table_csv)












#
# stock = Stock('DKNG', 'SMART', 'USD')
#
#
# market_data = ib.reqMktData(stock, "", False, False)


# ib.sleep(2)
# print(market_data)
# ib.pendingTickersEvent += get_real_time_info_on_stock
#
# ib.run()





#get history info on stock

# convert to pandas dataframe:
# df = util.df(bars)
# print(df)
# bars = ib.reqHistoricalData(
#     stock, endDateTime='', durationStr='30 D',
#     barSizeSetting='1 hour', whatToShow='MIDPOINT', useRTH=True)