import unittest
from binance_api import BinanceAPI
import time
import json

# in progress
class BackTestRunner(unittest.TestCase):
    def test_transactions(self):
        bm_test = BinanceAPI()
        bm_test.set_strategy()
        bm_test.set_logger("BCPTBTC")
        filename = "BCPTBTC-11-14-2020 23-30-23.txt"
        trade_dump = open("../logs/" + filename, "r")
        trades = trade_dump.readlines()

        for trade in trades:
            bm_test.handle_event(json.loads(trade))
            time.sleep(2)

        print("\n===========================================================\n")
        print(bm_test.get_all_transactions())
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")


if __name__ == '__main__':
    unittest.main()
