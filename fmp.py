import config
from helpers import get_jsonparsed_data, stock_types
from url_bank import get_url

STOCK_API_KEY = config.STOCK_API_KEY


def __get_data(type, **args):
    url = get_url(type, key=STOCK_API_KEY, **args)
    data = get_jsonparsed_data(url)
    return data


def get_rsi(stock):
    data = __get_data(stock_types.rsi, stock=stock)
    if data != None and len(data) > 0:
        return data[0]['rsi']
    return 0


def get_ema(stock, period=14):
    data = __get_data(stock_types.ema, stock=stock, period=period)
    if data != None and len(data) > 0:
        return data[0]['ema']
    return 0


def get_sma(stock, period=14):
    data = __get_data(stock_types.sma, stock=stock, period=period)
    if data != None and len(data) > 0:
        return data[0]['sma']
    return 0


def get_price(stock):
    data = __get_data(stock_types.price, stock=stock)
    if data != None and len(data) > 0:
        return data[0]['price']
    return 0


def get_gainers():
    return __get_data(stock_types.market_gainer)


def get_losers():
    return __get_data(stock_types.market_loser)


def screen_stocks(marketCapMoreThan=3000000000, marketCapLowerThan=10000000000, betaLowerThan=1, volumeMoreThan=1000000, dividendMoreThan=2, dividendLowerThan=4, priceMoreThan=50, limit=10):
    return __get_data(stock_types.stock_screener, marketCapMoreThan=marketCapMoreThan, marketCapLowerThan=marketCapLowerThan, betaLowerThan=betaLowerThan, volumeMoreThan=volumeMoreThan, dividendLowerThan=dividendLowerThan, dividendMoreThan=dividendMoreThan, priceMoreThan=priceMoreThan,
                      isActivelyTrading=True, isETF=True,
                      limit=limit)
