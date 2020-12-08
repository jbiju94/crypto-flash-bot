import json
import config
from logger import Logger
from account import Account
from connection import ConnectionManager
from trade import TradeSession
from strategy.pcent import PCent


class BinanceAPI:

    def __init__(self):
        self.__trade_pair = None
        self.__trade_session = None
        self.__quote_currency = None
        self.__asset = None
        self.__logger = None
        self.__strategy = PCent()
        client = ConnectionManager.get_client()
        Account.get_balance(client, "BTC")
        #Account.get_balance(client, "USDT")
        Account.print_balances()

    def set_logger(self, trade_pair: str):
        self.__logger = Logger(trade_pair)

    def set_strategy(self):
        self.__strategy = PCent()

    def start_session(self, asset: str, quote: str):
        self.__asset: str = asset
        self.__quote_currency: str = quote
        self.__trade_pair = str(self.__asset + self.__quote_currency)
        self.set_logger(self.__trade_pair)
        if config.MODE_WATCH_ONLY:
            self.__trade_session = None
        else:
            balance = float(Account.get_balance(ConnectionManager.get_client(), self.__quote_currency)['free'])
            Account.load_trade_pair_info(ConnectionManager.get_client(), self.__trade_pair)
            self.__trade_session = TradeSession(self.__asset,  self.__quote_currency, initial_buy=balance)
            self.__strategy.on_start(client=ConnectionManager.get_client(),
                                     trade=self.__trade_session)

        ConnectionManager.subscribe_to_stream(self.__trade_pair, on_event_fn=self.handle_event)

    def handle_event(self, event):
        if event['e'] == 'error':
            self.__trade_session.dump_position()

        else:
            self.__strategy.calculate_indicators(event)
            self.__logger.log_price(event)
            self.__strategy.react_to_signal(self.__trade_session)

