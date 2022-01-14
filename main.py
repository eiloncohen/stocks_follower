from ib_insync import *
import pandas
from datetime import datetime
import schedule
import time
from real_time_data import RealTimeData


def job():

    # read data from stocks file and enter it to list
    real_time_data_obj = RealTimeData()

    # connect to interactive brokers
    real_time_data_obj.connection()

    for i, stock in enumerate(real_time_data_obj.stocks_list):
        real_time_data_obj.set_real_time_info_on_stock(stock, i)

    real_time_data_obj.update_csv_table_and_close_connection()


job()
schedule.every(5).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)