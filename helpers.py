from types import SimpleNamespace
from urllib.request import urlopen
import json

states = SimpleNamespace(**{
    'buy': 'BUY',
    'sell': 'SELL',
    'hold': 'HOLD'
})


oversold_limit = 50
# replace it with your prefered oversold threshold - recommended > 30
oversold_threshold = 30
# replace it with your prefered overbought threshold -recommended < 70
overbought_threshold = 50


def checkRSI(rsi):
    if rsi > oversold_threshold and rsi < oversold_limit:
        return states.buy
    elif rsi > overbought_threshold:
        return states.sell
    else:
        return states.hold


def checkMA(ma_50, ma_200):
    if ma_50 > ma_200:  # golden cross
        return states.buy
    elif ma_50 < ma_200:  # death cross
        return states.sell
    else:
        return states.hold


def checKMACD(macd):
    if macd > 0:
        return states.buy
    elif macd < 0:
        return states.sell
    else:
        return states.hold


def checkATR(atr, sma):
    if (atr > sma):
        return states.buy
    return states.hold


def get_jsonparsed_data(url):
    try:
        response = urlopen(url)
        data = response.read().decode("utf-8")
        return json.loads(data)
    except Exception as e:
        print("Error fetching data from url %s" % url)
        print(e.__dict__)
        return None


stock_types = SimpleNamespace(**{
    'atr': 'atr',
    'sma': 'sma',
    'rsi': 'rsi',
    'ema': 'ema',
    'market_gainer': 'market_gainer',
    'market_loser': 'market_loser',
    'stock_screener': 'stock_screener'
})
