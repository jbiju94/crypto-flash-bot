class Account:
    __balances = list()
    __asset_info = list()

    @staticmethod
    def __load_balance(client, asset):
        balance = client.get_asset_balance(asset)
        Account.__balances.append(balance)

        return balance

    @staticmethod
    def get_balance(client, asset: str = "BTC"):
        balances = list(Account.__balances)
        return next((asset_balance for asset_balance in balances if asset_balance['asset'] == asset),
                    Account.__load_balance(client, asset))

    @staticmethod
    def load_trade_pair_info(client, pair=None):
        if pair is not None:
            Account.__asset_info.append(client.get_symbol_info(pair))

    @staticmethod
    def get_trade_pair_info(pair):
        return next((asset_info for asset_info in Account.__asset_info if asset_info['symbol'] == pair), None)

    @staticmethod
    def get_lot_size_info(pair) -> (float, float, float):
        asset_info = Account.get_trade_pair_info(pair)
        lot_size = next((_filter for _filter in asset_info['filters'] if _filter['filterType'] == "LOT_SIZE"), None)
        if lot_size is not None:
            return float(lot_size['minQty']), float(lot_size['maxQty']), float(lot_size['stepSize'])
        else:
            return 0, 0, 0

    @staticmethod
    def print_balances():
        print("\n================== BALANCE ==================\n")
        for balance in Account.__balances:
            print(balance)
        print("\n=============================================\n")
