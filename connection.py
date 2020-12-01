from binance.client import Client
from binance.websockets import BinanceSocketManager

import config
import credentails


class ConnectionManager:
    __binance_client = None
    __binance_socket_manager = None
    __connection_key = None

    @staticmethod
    def get_client():
        if ConnectionManager.__binance_client is None :
            connection_success = ConnectionManager.__connect_to_binance()
            if connection_success:
                return ConnectionManager.__binance_client
            else:
                return None

        else:
            return ConnectionManager.__binance_client

    @staticmethod
    def __connect_to_binance():
        ConnectionManager.__binance_client = Client(credentails.binance_api_key, credentails.binance_api_secret)
        if config.MODE_TEST_NET:
            ConnectionManager.__binance_client.API_URL = "https://testnet.binance.vision/api"
            print("> Connected to Test Net")
        return ConnectionManager.__test_connection(ConnectionManager.__binance_client)

    @staticmethod
    def __test_connection(client) -> bool:
        try:
            client.ping()
        except Exception as e:
            print("> ERROR: Client Initialized Failed - {}".format(e))
            return False
        else:
            print("> Client Initialized.")
            return True

    @staticmethod
    def subscribe_to_stream(trade_pair, on_event_fn):
        print("> Listening to trades of '{}'.".format(trade_pair))
        print("================================================")
        ConnectionManager.__binance_socket_manager = BinanceSocketManager(ConnectionManager.get_client())
        ConnectionManager.__connection_key = \
            ConnectionManager.__binance_socket_manager.start_trade_socket(trade_pair, on_event_fn)
        ConnectionManager.__binance_socket_manager.start()
