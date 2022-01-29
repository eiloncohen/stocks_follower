from interactive_info import *

TOTAL_SIZE = int(DURATION.split(" ")[0]) - 1
PERCENTAGE = 0.982


class StockInfo:
    def __init__(self, tiker):
        self.stock = Stock(tiker, 'SMART', 'USD')
        self.history_info_on_stock = None

    def check_bullish_engulfing_pattern(self):
        for (index, row) in self.history_info_on_stock.iterrows():
            is_down = self.check_down_for_few_days()
            if is_down["is_down"]:
                # get the last candle in the down side
                specefic_red_candle = self.history_info_on_stock[self.history_info_on_stock['date'] == is_down['row_date']]

                # get the index of the last candle
                idx = self.history_info_on_stock.index[self.history_info_on_stock['date'] == is_down['row_date']]

                # get the next candle to check bullish engulfing pattern
                next_candle = self.history_info_on_stock.iloc[idx + 1]

                # check if both two candles are marboush
                is_both_marboush = self.check_id_two_candels_marbush(specefic_red_candle, next_candle)

                if is_both_marboush:
                    is_second_candle_bigger = self.is_second_candle_bigger(specefic_red_candle, next_candle)
                    if is_second_candle_bigger['is_second_candle_bigger']:
                        print("bullish engulfing found!!! in date: " + is_second_candle_bigger['date'].strftime("%d/%m/%Y"))
                        break
                else:
                        print("bullish engulfing no found")



    def check_down_for_few_days(self):
        is_down = False
        idx = 0
        for (index, row) in self.history_info_on_stock.iterrows():
            index = idx
            if idx + 1 < TOTAL_SIZE:
                while self.history_info_on_stock.iloc[idx]['close'] > self.history_info_on_stock.iloc[idx + 1]['close']:
                    idx += 1
                if idx > index + 3:
                    index = idx
                    is_down = True
                    return {"is_down": is_down, "row_date": self.history_info_on_stock.iloc[idx]['date'],
                            "last_index": index}
                else:
                    idx += 1
                    pass

        return {"is_down": is_down, "row_date": "None"}

    def check_is_exist_marboush_candels_in_stock(self):
        marboush_dict = {
            'dates': [],
            'count_of_candels': 0
        }
        for (index, row) in self.history_info_on_stock.iterrows():
            current_dict = {'date': row.date, 'open': row.open, 'low': row.low, 'high': row.high, 'close': row.close}
            is_marcoush_candle = self.is_marboush_candle(current_dict)
            if is_marcoush_candle['is marbush candle']:
                marboush_dict['count_of_candels'] += 1
                marboush_dict['dates'].append(is_marcoush_candle['date'])
        return marboush_dict

    def is_marboush_candle(self, current_dict):
        is_marboush = False
        open_price = round(current_dict['open'], 2)
        high_price = round(current_dict['high'], 2)
        close_price = round(current_dict['close'], 2)
        low_price = round(current_dict['low'], 2)

        # berish marboush
        if (high_price * PERCENTAGE <= open_price or open_price == high_price) and (
                close_price * PERCENTAGE <= low_price or low_price == close_price):
            is_marboush = True

        # buliish marboush
        if (high_price * PERCENTAGE <= close_price or close_price == high_price) and (
                open_price * PERCENTAGE <= low_price or low_price == open_price):
            is_marboush = True
        return {'is marbush candle': is_marboush, 'date': current_dict['date']}

    def check_id_two_candels_marbush(self, first_candle, second_candle):
        is_first_candle_marboush = False
        is_second_candle_marboush = False
        for (index, row) in first_candle.iterrows():
            current_dict = {'date': row.date, 'open': row.open, 'low': row.low, 'high': row.high, 'close': row.close}
            is_first_candle_marboush = self.is_marboush_candle(current_dict)

        for (index, row) in second_candle.iterrows():
            current_dict = {'date': row.date, 'open': row.open, 'low': row.low, 'high': row.high, 'close': row.close}
            is_second_candle_marboush = self.is_marboush_candle(current_dict)

        if is_first_candle_marboush and is_second_candle_marboush:
            return True
        else:
            return False

    def is_second_candle_bigger(self, specefic_red_candle, next_candle):
        specefic_red_candle_dict = {}
        next_candle_dict = {}
        for (index, row) in specefic_red_candle.iterrows():
            specefic_red_candle_dict = {'date': row.date, 'open': row.open, 'low': row.low, 'high': row.high,
                                        'close': row.close}

        for (index, row) in next_candle.iterrows():
            next_candle_dict = {'date': row.date, 'open': row.open, 'low': row.low, 'high': row.high,
                                'close': row.close}

        if specefic_red_candle_dict['open'] > next_candle_dict['open'] and specefic_red_candle_dict['close'] < \
                next_candle_dict['close'] and specefic_red_candle_dict['low'] > next_candle_dict['low'] and \
                specefic_red_candle_dict['high'] < next_candle_dict['high']:
            return {'is_second_candle_bigger': True, 'date': next_candle_dict['date']}
        else:
            return {'is_second_candle_bigger': False, 'date': next_candle_dict['date']}
