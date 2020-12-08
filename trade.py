from utility import percentage_change
import math
from connection import ConnectionManager
import collections, functools, operator
from account import Account
from decimal import getcontext, ROUND_DOWN, Decimal


class TradeSession:

    def __init__(self,  asset: str, quote: str, initial_buy: float):
        self.asset: str = asset
        self.quote_currency: str = quote
        self.trade_pair: str = str(asset + quote)
        self.all_trades = list()
        self.my_trades = list()
        self.exit_prices = list()

        # make initial buy
        (self.entry_price, self.entry_quantity) = self.__execute_market_buy(initial_buy)
        self.remaining_quantity = self.entry_quantity

    def average_exit_price(self) -> float:
        try:
            sum(self.exit_prices) / len(self.exit_prices)
        except ZeroDivisionError:
            return 0.0

    def __execute_market_buy(self, quote_quantity: float) -> (float, float):
        print("> Posting Buy Order")
        client = ConnectionManager.get_client()
        qty = self.round_quantity()

        order = client.order_market_buy(
            symbol=self.trade_pair,
            quantity=qty
        )
        print(order)

        # avg_entry_price = dict(functools.reduce(operator.add, map(collections.Counter, order['fills'])))['price']
        avg_entry_price = order['fills'][0]['price']
        qty = order['fills'][0]["qty"]

        print("> Trade Confirmed : Buy @ {} (MarketPrice) Executed for '{}'.".format(order['price'], self.trade_pair))
        self.my_trades.append(order)
        return float(avg_entry_price), float(qty)

    def execute_market_sell(self, quantity_percent: float):
        print("> Posting Sell Order")
        sell_qty = float(self.remaining_quantity * (quantity_percent / 100))

        order = ConnectionManager.get_client().order_market_sell(
            symbol=self.trade_pair,
            quantity=sell_qty)

        self.exit_prices.append(order['price'])
        self.remaining_quantity = float(self.remaining_quantity) - float(order['executedQty'])
        self.my_trades.append(order)
        print("> Trade Confirmed : Sell @ {} (MarketPrice) Executed for '{}'.".format(order['price'], self.trade_pair))
        print("> Remaining Quantity: {}".format(self.remaining_quantity))

    def execute_limit_sell(self, price: float):
        print("> Posting Limit Sell Order")
        client = ConnectionManager.get_client()
        qty = self.round_quantity_1(asset=self.asset)

        order = client.order_limit_sell(
                    symbol=self.trade_pair,
                    quantity=qty,
                    price="{:.8f}".format(price))
        print(order)
        print("> Limit Sell Posted @ {} (MarketPrice) Executed for '{}'.".format(price, self.trade_pair))

    def dump_position(self):
        print("> ** Dumping Position **")
        self.execute_market_sell(100)


    """ def round_quantity(self, quantity: float) -> float:
        fee_percent = 0.9995
        balance = 0.00000020 * fee_percent#Account.get_balance(client=ConnectionManager.get_client(), asset=self.quote_currency)
        #balance = float(balance['free']) * fee_percent
        return balance
"""
    def round_quantity(self) -> float:
        fee_percent = 0.9995
        min_qty, max_qty, step_size = Account.get_lot_size_info(pair=self.trade_pair)
        balance = Account.get_balance(client=ConnectionManager.get_client(), asset=self.quote_currency)['free']
        trades = ConnectionManager.get_client().get_recent_trades(symbol=self.trade_pair)
        quantity = (float(balance)) / float(trades[0]['price']) * fee_percent
        precision = int(round(-math.log(step_size, 10), 0))
        return round(quantity, precision)

    def round_quantity_1(self, asset) -> float:
        fee_percent = 0.9995
        min_qty, max_qty, step_size = Account.get_lot_size_info(pair=self.trade_pair)
        balance = Account.get_balance(client=ConnectionManager.get_client(), asset=asset)['free']
        trades = ConnectionManager.get_client().get_recent_trades(symbol=self.trade_pair)
        quantity = (float(balance)) * fee_percent
        precision = int(round(-math.log(step_size, 10), 0))
        return round(quantity, precision)


    def print_trade_session_summary(self):
        avg_exit_price = self.average_exit_price()
        print("++++++++++++++++++++++++ Summary ++++++++++++++++++++++++++")
        print("|> Entry Price: {}".format(self.entry_price))
        print("|> Entry Qty: {}".format(self.entry_quantity))
        print("|> Exit Prices: {}".format(self.exit_prices))
        print("|> Exit Prices: {}".format(self.exit_prices))
        print("|> Average Exit Price: {}".format(avg_exit_price))
        print("|> Remaining Qty: {}".format(self.remaining_quantity))
        print("===========================================================")
        print("|> Return : {}%".format(percentage_change(avg_exit_price, self.entry_price)))
        print("===========================================================")
        print("==================++  TRANSACTIONS   ======================")
        for transaction in self.my_trades:
            print("|>>> {}".format(transaction))
        print("===========================================================")
