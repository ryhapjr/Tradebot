import config
from helpers import get_jsonparsed_data, stock_types
from url_bank import get_url
from datetime import date, timedelta

STOCK_API_KEY = config.ALPHA_ADVANTAGE_KEY


def __get_data(type, **args):
    url = get_url(type, key=STOCK_API_KEY, **args)
    data = get_jsonparsed_data(url)
    return data


def get_atr(stock, period=14):
    data = __get_data(stock_types.atr, symbol=stock, period=period)
    if data is None:
        return 0
    today = date.today()
    yesterday = today - timedelta(days=1)
    dataKey = str(yesterday)
    atr = data['Technical Analysis: ATR'][dataKey]['ATR']
    return float(atr)
