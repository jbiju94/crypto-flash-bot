from datetime import datetime
from config import LOG_PRICE_STREAM_TO_FILE, LOG_PRICE_STREAM
import json


class Logger:

    def __init__(self, trade_pair):
        self.__log_file_handler = None
        self.__filename: str = trade_pair + "-" + datetime.now().strftime("%m-%d-%Y %H-%M-%S") + ".txt"
        if LOG_PRICE_STREAM_TO_FILE:
            self.__log_file_handler = open("./logs/" + self.__filename, "a")
        else:
            self.__log_file_handler = None

    def log_price(self, event):
        if self.__log_file_handler is not None:
            self.__log_file_handler.write(json.dumps(event))
            self.__log_file_handler.write("\n")

        Logger.log_price_stream(event)

    @staticmethod
    def log_price_stream(event):
        if LOG_PRICE_STREAM:
            # trade_time = datetime.fromtimestamp(int(event['T'] / 1000)).strftime('%Y-%m-%d %H:%M:%S')
            trade_time = event['T']
            event_time = event['E']
            diff = int(event['E']) - int(event['T'])
            current_price = float(event['p'])
            print("[Trade: {} | Event: {} | Diff: {}ms ] {} | Price: {:.8f}".format(trade_time, event_time, diff, event['e'], current_price))
        else:
            pass

    def __del__(self):
        if self.__log_file_handler is not None:
            self.__log_file_handler.close()
