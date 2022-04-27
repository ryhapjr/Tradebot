from string import Template
from helpers import stock_types

rsi_url = Template(
    'https://financialmodelingprep.com/api/v3/technical_indicator/15min/$stock?period=10&type=rsi&apikey=$key')

sma_url = Template(
    'https://financialmodelingprep.com/api/v3/technical_indicator/daily/$stock?period=$period&type=sma&apikey=$key')

ema_url = Template(
    'https://financialmodelingprep.com/api/v3/technical_indicator/daily/$stock?period=10&type=ema&apikey=$key')
market_gainer_url = Template(
    'https://financialmodelingprep.com/api/v3/stock_market/gainers?apikey=$key')
market_loser_url = Template(
    'https://financialmodelingprep.com/api/v3/stock_market/losers?apikey=$key')
stock_screener_url = Template(
    'https://financialmodelingprep.com/api/v3/stock-screener?marketCapMoreThan=$marketCapMoreThan&marketCapLowerThan=$marketCapLowerThan&betaLowerThan=$betaLowerThan&volumeMoreThan=$volumeMoreThan&dividendMoreThan=$dividendMoreThan&dividendLowerThan=$dividendLowerThan&priceMoreThan=$priceMoreThan&isActivelyTrading=True&limit=$limit&apikey=$key')

atr_url = Template(
    'https://www.alphavantage.co/query?function=ATR&symbol=$symbol&interval=daily&time_period=$period&apikey=$key')


url_by_type = {
    stock_types.rsi: rsi_url,
    stock_types.ema: ema_url,
    stock_types.market_gainer: market_gainer_url,
    stock_types.market_loser: market_loser_url,
    stock_types.stock_screener: stock_screener_url,
    stock_types.sma: sma_url,
    stock_types.atr: atr_url
}


def get_url(type, **args):
    url_base = url_by_type[type]
    url = url_base.substitute(**args)
    return url
