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
