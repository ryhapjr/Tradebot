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


def checkToBuy(ema_21, sma_20, sma_50, sma_100, sma_200, rsi, macd):
    if ema_21 > sma_20 and sma_20 > sma_50 and ema_21 > sma_50 and sma_50 > sma_100 and sma_100 > sma_200 and rsi > 55 and macd > 0:
        return True

    return False


def checkToSell(price, sma_50):
    if price <= sma_50:
        return True
    return False


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
    'stock_screener': 'stock_screener',
    'price': 'price',
    'macd': 'macd'
})
