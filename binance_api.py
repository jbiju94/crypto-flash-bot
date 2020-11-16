import json
from datetime import datetime

from binance.client import Client
from binance.enums import *
from binance.websockets import BinanceSocketManager

import config
import credentails
from utility import log_price_stream


class BinanceAPI:

    def __init__(self):
        # Connection Related

        self.__client = Client(credentails.binance_api_key, credentails.binance_api_secret)
        self.__trade_pair = None
        self.__bm = None
        self.__connection_key = None

        # Position Related
        self.__entry_timestamp = None
        self.__entry_price = None
        self.__entry_quantity = None
        self.__exit_prices = list()
        self.__remaining_quantity = None

        # Stream Related
        self.__last_trade_price = None
        self.__trade_history = list()
        self.__dump_trend_counter = 0
        self.__transactions = list()
        self.__log_file_handler = None
        try:
            self.__client.ping()
        except Exception as e:
            print("> ERROR: Client Initialized Failed - {}".format(e))
        else:
            print("> Client Initialized.")
            print(self.__client.get_server_time())
            print(self.__client.get_asset_balance(asset='BTC'))
            print(self.__client.get_asset_balance(asset='USDT'))

    def start_session(self, trade_pair: str):
        self.__trade_pair = trade_pair
        if not config.MODE_WATCH_ONLY:
            self.__execute_market_buy(100)

        filename: str = trade_pair + "-" + datetime.now().strftime("%m-%d-%Y %H-%M-%S") + ".txt"
        self.__log_file_handler = open("./logs/" + filename, "a")
        self.__stream_trades()

    def __stream_trades(self):
        print("> Listening to trades of '{}'.".format(self.__trade_pair))
        print("================================================")
        self.__bm = BinanceSocketManager(self.__client)
        self.__connection_key = self.__bm.start_trade_socket(self.__trade_pair, self.handle_event)
        self.__bm.start()

    def __execute_market_buy(self, quantity: float):
        order = self.__client.create_test_order(
            symbol=self.__trade_pair,
            side=SIDE_BUY,
            type=ORDER_TYPE_MARKET,
            timeInForce=TIME_IN_FORCE_GTC,
            quantity=quantity)
        print(order)
        self.__remaining_quantity = order['executedQty']
        self.__entry_timestamp = datetime.now()
        self.__entry_price = order['price']
        self.__entry_quantity = order['executedQty']
        self.__transactions.append(order)
        print("> Buy @ {} (MarketPrice) Executed for '{}'.".format(order['price'], self.__trade_pair))

    def __execute_market_sell(self, quantity: float):
        order = self.__client.create_order(
            symbol=self.__trade_pair,
            side=SIDE_SELL,
            type=ORDER_TYPE_MARKET,
            timeInForce=TIME_IN_FORCE_GTC,
            quantity=quantity)
        print(order)
        self.__exit_prices.append(order['price'])
        self.__remaining_quantity = float(self.__remaining_quantity) - float(order['executedQty'])
        self.__transactions.append(order)
        print("> Sell @ {} (MarketPrice) Executed for '{}'.".format(order['price'], self.__trade_pair))

    def handle_event(self, event):
        if event['e'] == 'error':
            self.dump_position()

        else:
            if self.__last_trade_price is None:
                self.__last_trade_price = float(event['p'])
            elif self.__last_trade_price != float(event['p']):
                self.__process(event)
                log_price_stream(event, self.__entry_price)
                self.__trade_history.append(event)
                if config.LOG_TRADE_HISTORY:
                    self.__log_file_handler.write(json.dumps(event))
                    self.__log_file_handler.write("\n")
            else:
                pass

    def dump_position(self):
        print("** Bot Exit Signal **")
        if not config.MODE_WATCH_ONLY:
            ip = input("Exiting Position..")
            if ip.lower() == 'y':
                self.__execute_market_sell(quantity=float(self.__remaining_quantity))
            self.__show_summary()
            self.__log_file_handler.close()
            self.__bm.stop_socket(self.__connection_key)

    def __process(self, event):
        current_price = float(event['p'])

        if self.__last_trade_price > current_price:
            # Scenario: Price Decreasing
            self.__dump_trend_counter = self.__dump_trend_counter + 1
            print("Last Price: %.8f < Current Price: %.8f | Increasing DUMP_IND to % .2d" % (
            self.__last_trade_price, current_price, self.__dump_trend_counter))
        else:
            # Scenario: Price Increasing
            self.__dump_trend_counter = self.__dump_trend_counter - 1
            print("Last Price: %.8f > Current Price: %.8f | Decreasing DUMP_IND to % .2d" % (
            self.__last_trade_price, current_price, self.__dump_trend_counter))

        self.__last_trade_price = current_price

        if self.__dump_trend_counter > config.DUMP_TREND_THRESHOLD:
            print("> Dump detected.")
            print("> Exiting Position..")
            if not config.MODE_WATCH_ONLY:
                self.__execute_market_sell(quantity=float(self.__remaining_quantity))
                print("> Stopping Trade Stream")
                self.__show_summary()
                self.__bm.stop_socket(self.__connection_key)
                self.__log_file_handler.close()
                return

        elif self.__dump_trend_counter == config.SHORT_DUMP_TREND_THRESHOLD:
            print("> Down trend detected.")
            print("> Selling 50%..")
            if not config.MODE_WATCH_ONLY:
                self.__execute_market_sell(quantity=float(self.__remaining_quantity * 0.50))

        else:
            return

    def __show_summary(self):
        # avg_exit_price = sum(self.__exit_prices) / len(self.__exit_prices)
        print("++++++++++++++++++++++++ Summary ++++++++++++++++++++++++++")
        print("|> Entry Price: {}".format(self.__entry_price))
        print("|> Entry Qty: {}".format(self.__entry_quantity))
        print("|> Exit Prices: {}".format(self.__exit_prices))
        # print("|> Average Exit Price: {}".format(avg_exit_price))
        print("|> Remaining Qty: {}".format(self.__remaining_quantity))
        print("|> Exit Timestamp: {}".format(datetime.now()))
        print("===========================================================")
        # print("|> Return : {}%".format(percentage_change(avg_exit_price, self.__entry_price)))
        print("===========================================================")
        print("==================++  TRANSACTIONS   ======================")
        for transaction in self.__transactions:
            print("|>>> {}".format(transaction))
        print("===========================================================")
        print(self.__client.get_trade_fee(symbol=self.__trade_pair))

    def get_all_transactions(self) -> list:
        return self.__transactions
