from datetime import datetime

import config


def percentage_change(buy_price: float, current_price: float):
    if buy_price == current_price:
        return 0
    try:
        _change = ((current_price - buy_price) / buy_price) * 100.0
        return round(_change, 2)
    except ZeroDivisionError:
        return float('inf')


def log_price_stream(event, entry_price: float):
    if config.LOG_PRICE_STREAM:
        date_time = datetime.fromtimestamp(int(event['T'] / 1000)).strftime('%Y-%m-%d %H:%M:%S')
        current_price = float(event['p'])
        if config.LOG_PRICE_CHANGE:
            change = percentage_change(entry_price, current_price)
            print("[{}] {} | Price: {} ({}%)".format(date_time, event['e'], current_price, change))
        else:
            print("[{}] {} | Price: {}".format(date_time, event['e'], current_price))
    else:
        pass


def dump_trade_stream_logs(stream):
    filename = datetime.now() + ".txt"
    stream_log = open(filename, "w")
    stream_log.writelines(stream)
    file1.close()