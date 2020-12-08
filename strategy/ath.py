from strategy import StrategyBase
from config import MODE_WATCH_ONLY
from trade import TradeSession


class ATH:
    DUMP_TREND_THRESHOLD = 10
    SHORT_DUMP_TREND_THRESHOLD = 5

    def __init__(self):
        print("> Strategy: All Time High")
        # Indicators
        self.__last_trade_price = None
        self.__dump_trend_counter = 0
        self.ath = None

    def calculate_indicators(self, params):
        if self.__last_trade_price is None:
            self.__last_trade_price = float(params['p'])
            self.ath = self.__last_trade_price
        else:
            current_price = float(params['p'])

            # new All Time High
            if current_price > self.ath:
                self.ath = current_price
                self.__dump_trend_counter = 0
                print("> New ATH : {:.8f} ".format(self.ath))

            elif current_price == self.ath:
                self.__dump_trend_counter = 0
                print("> Price = ATH: {:.8f} | Reset Indicator ! : {} "
                      .format(current_price, self.__dump_trend_counter))

            elif self.ath - current_price == 0.00000001:
                self.__dump_trend_counter = self.__dump_trend_counter - 2
                print("> Price near ATH: {:.8f} |  Indicator --2 : {} "
                      .format(current_price, self.__dump_trend_counter))

            else:
                # if current price is less that the last price - price reduced.
                if current_price < self.__last_trade_price:
                    self.__dump_trend_counter = self.__dump_trend_counter + 1
                    print("> Price: {:.8f} | Indicator ++ : {} "
                          .format(current_price, self.__dump_trend_counter))
                elif current_price == self.__last_trade_price:
                    pass
                # if current price is increased than the previous price - price increased .
                else:
                    self.__dump_trend_counter = self.__dump_trend_counter - 1
                    print("> Indicator -- : {} ".format(self.__dump_trend_counter))

        self.__last_trade_price = float(params['p'])

    def react_to_signal(self, trade_session: TradeSession):
        if not MODE_WATCH_ONLY :
            if self.__dump_trend_counter > ATH.DUMP_TREND_THRESHOLD:
                print("> Dump detected | Exiting Position..")
                if trade_session is not None:
                    trade_session.execute_market_sell(quantity_percent=100)

            elif self.__dump_trend_counter == ATH.SHORT_DUMP_TREND_THRESHOLD:
                print("> Down trend detected. Selling 50%..")
                if trade_session is not None:
                    trade_session.execute_market_sell(quantity_percent=50)
                    print("> Remaining Quantity: {}".format(self.__remaining_quantity))

        else:
            pass
