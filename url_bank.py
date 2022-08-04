from string import Template
from helpers import stock_types

rsi_url = Template(
    'https://financialmodelingprep.com/api/v3/technical_indicator/1min/$stock?period=10&type=rsi&apikey=$key')

sma_url = Template(
    'https://financialmodelingprep.com/api/v3/technical_indicator/1min/$stock?period=$period&type=sma&apikey=$key')
price_url = Template(
    'https://financialmodelingprep.com/api/v3/quote-short/$stock?apikey=$key')

ema_url = Template(
    'https://financialmodelingprep.com/api/v3/technical_indicator/1min/$stock?period=$period&type=ema&apikey=$key')
market_gainer_url = Template(
    'https://financialmodelingprep.com/api/v3/stock_market/gainers?apikey=$key')
market_loser_url = Template(
    'https://financialmodelingprep.com/api/v3/stock_market/losers?apikey=$key')
stock_screener_url = Template(
    'https://financialmodelingprep.com/api/v3/stock-screener?marketCapMoreThan=$marketCapMoreThan&marketCapLowerThan=$marketCapLowerThan&betaLowerThan=$betaLowerThan&volumeMoreThan=$volumeMoreThan&dividendMoreThan=$dividendMoreThan&dividendLowerThan=$dividendLowerThan&priceMoreThan=$priceMoreThan&isActivelyTrading=True&limit=$limit&apikey=$key')

atr_url = Template(
    'https://www.alphavantage.co/query?function=ATR&symbol=$symbol&interval=1min&time_period=$period&apikey=$key')
macd_url = Template(
    'https://www.alphavantage.co/query?function=MACDEXT&symbol=$symbol&interval=1min&series_type=close&&apikey=$key')


url_by_type = {
    stock_types.rsi: rsi_url,
    stock_types.ema: ema_url,
    stock_types.market_gainer: market_gainer_url,
    stock_types.market_loser: market_loser_url,
    stock_types.stock_screener: stock_screener_url,
    stock_types.sma: sma_url,
    stock_types.atr: atr_url,
    stock_types.price: price_url,
    stock_types.macd: macd_url
}


def get_url(type, **args):
    url_base = url_by_type[type]
    url = url_base.substitute(**args)
    return url
