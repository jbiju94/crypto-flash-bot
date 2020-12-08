from strategy import StrategyBase
from config import MODE_WATCH_ONLY
from trade import TradeSession


class PCent:
    DUMP_TREND_THRESHOLD = 10
    SHORT_DUMP_TREND_THRESHOLD = 5

    def __init__(self):
        print("> Strategy: Percent")
        # Indicators
        self.__p_cent = 0.10
        self.__buy_price = None
        self.__sell_price = None
        self.__symbol = None

    def on_start(self, client=None, trade: TradeSession = None):
        self.__symbol = trade.trade_pair
        self.__buy_price = float(trade.entry_price)
        self.__sell_price = float((self.__buy_price * self.__p_cent) + self.__buy_price)
        # Apply Limit Orders
        trade.execute_limit_sell(self.__sell_price)

    def calculate_indicators(self, params):
        pass

    def react_to_signal(self, trade_session: TradeSession):
        pass
