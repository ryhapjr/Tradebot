from urllib.request import urlopen
import json
import config
from string import Template
from types import SimpleNamespace

STOCK_API_KEY = config.STOCK_API_KEY


def __get_jsonparsed_data(url):
    response = urlopen(url)
    data = response.read().decode("utf-8")
    return json.loads(data)


rsi_url = Template(
    'https://financialmodelingprep.com/api/v3/technical_indicator/daily/$stock?period=10&type=rsi&apikey=$key')
ema_url = Template(
    'https://financialmodelingprep.com/api/v3/technical_indicator/daily/$stock?period=10&type=ema&apikey=$key')
market_gainer_url = Template(
    'https://financialmodelingprep.com/api/v3/stock_market/gainers?apikey=$key')
market_loser_url = Template(
    'https://financialmodelingprep.com/api/v3/stock_market/losers?apikey=$key')
stock_screener_url = Template(
    'https://financialmodelingprep.com/api/v3/stock-screener?marketCapMoreThan=$marketCapMoreThan&betaMoreThan=$betaMoreThan&volumeMoreThan=$volumeMoreThan&dividendMoreThan=$dividendMoreThan&limit=$limit&apikey=$key')


stock_types = SimpleNamespace(**{
    'rsi': 'rsi',
    'ema': 'ema',
    'market_gainer': 'market_gainer',
    'market_loser': 'market_loser',
    'stock_screener': 'stock_screener'
})


url_by_type = {
    stock_types.rsi: rsi_url,
    stock_types.ema: ema_url,
    stock_types.market_gainer: market_gainer_url,
    stock_types.market_loser: market_loser_url,
    stock_types.stock_screener: stock_screener_url
}


def __get_url(type, **args):
    url_base = url_by_type[type]
    url = url_base.substitute(key=STOCK_API_KEY, **args)
    return url


def __get_data(type, **args):
    url = __get_url(type, **args)
    data = __get_jsonparsed_data(url)
    return data


def get_rsi(stock):
    return __get_data(stock_types.rsi, stock=stock)


def get_ema(stock):
    return __get_data(stock_types.ema, stock=stock)


def get_gainers():
    return __get_data(stock_types.market_gainer)


def get_losers():
    return __get_data(stock_types.market_loser)


def screen_stocks(marketCapMoreThan=1000, betaMoreThan=1, volumeMoreThan=10000, dividendMoreThan=0, limit=10):
    return __get_data(stock_types.stock_screener, marketCapMoreThan, betaMoreThan, volumeMoreThan, dividendMoreThan, limit)
