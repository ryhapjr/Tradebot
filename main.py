from ensurepip import version
import config
from config import *
import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import REST, TimeFrame, TimeFrameUnit
import numpy as np
import time
# import ast
# import json
import talib as ta
import time
from datetime import datetime, timedelta
from types import SimpleNamespace


API_KEY = config.API_KEY
SECRET_KEY = config.API_SECRET_KEY
BASE_URL = config.BASE_URL  # base URL for paper trading
# For real trading, do not enter a base URL
api = REST(key_id=API_KEY, secret_key=SECRET_KEY, base_url=BASE_URL)


rsi_timeframe = 14  # replace it with your prefered timeframe for RSI
oversold_limit = 50
# replace it with your prefered oversold threshold - recommended > 30
oversold_threshold = 30
# replace it with your prefered overbought threshold -recommended < 70
overbought_threshold = 50
# company = "AAPL"  # "AAPL" #replace it with your prefered company symbol from: https://www.nyse.com/listings_directory/stock
shares = 1  # replace it with your prefered number of shares to buy/sell
data = []  # should be reseted every time you start the bot
days = 30  # replace it with your prefered number of days to calculate RSI
api_time_format = '%Y-%m-%d'


pos_held = False

states = SimpleNamespace(**{
    'buy': 'BUY',
    'sell': 'SELL',
    'hold': 'HOLD'
})

# list of stocks to trade on
# companies = ['AAPL', 'SPY']
companies = ['DOMO', 'TLRY', 'SQ', 'MRO', 'AAPL', 'GM', 'SNAP', 'SHOP',
                     'SPLK', 'BA', 'AMZN', 'SUI', 'SUN', 'TSLA', 'CGC', 'SPWR',
                     'NIO', 'CAT', 'MSFT', 'PANW', 'OKTA', 'TWTR', 'TM', 'RTN',
                     'ATVI', 'GS', 'BAC', 'MS', 'TWLO', 'QCOM', ]


def fetch_data(company, days):
    start_time, end_time = calculate_start_end(days)
    try:
        market_data = api.get_bars(
            company,
            TimeFrame.Day,
            start_time,
            end_time,
            limit=days
        )
        return market_data
    except Exception as e:
        print(e)
        return None


def calculate_start_end(days):
    now = datetime.now()
    start_time = (now.date() -
                  timedelta(days=days))
    end_time = (now.date() -
                timedelta(days=1)).strftime(api_time_format)
    return start_time, end_time


def calculate_moving_average(company, days):
    try:
        market_data = fetch_data(company, days * 2)
        if market_data == None:
            return 0
        close_prices = np.array(market_data.df['close'])
        sma = ta.SMA(close_prices, days)[-1]
        return sma
    except Exception as e:
        print(e)
        return 0


def calculate_rsi(data, timeframe):
    np_data = np.array(data)  # Convert to numpy array
    rsis = ta.RSI(np_data, timeframe)
    return rsis[-1]


def calculate_macd(company, days):
    try:
        market_data = fetch_data(company, days)
        if market_data == None:
            return 0
        close_prices = np.array(market_data.df['close'])

        macd, macdsignal, macdhist = ta.MACD(
            close_prices, fastperiod=12, slowperiod=26, signalperiod=9)
        print(macd[-1])
        print(macdsignal[-1])
        print(macdhist[-1])
        return macdhist[-1]

    except Exception as e:
        print(e)
        return 0


def checkRSI(rsi):
    if rsi > oversold_threshold and rsi < oversold_limit:
        return states.buy
    elif rsi > overbought_threshold:
        return states.sell
    else:
        return states.hold


def checkMA(ma, ma_50):
    if ma_50 > ma:  # golden cross
        return states.buy
    elif ma_50 < ma:  # death cross
        return states.sell
    else:
        return states.hold


def buyAndSell(company, days):
    print("Checking Price for " + company)

    ma = calculate_moving_average(company, 200)
    ma_50 = calculate_moving_average(company, 50)
    msc = calculate_macd(company, 60)

    # print(ma, ma_50)
    mast = checkMA(ma, ma_50)

    market_data = fetch_data(company, days)
    if market_data == None:
        print("No data for " + company)
        return

    data = market_data.df['close']

    if len(data) >= rsi_timeframe:
        rsi_now = calculate_rsi(data, rsi_timeframe)
        trade_state = checkRSI(rsi_now)

        print(mast, trade_state)

        if trade_state == states.buy:
            try:
                orders = api.list_orders(symbols=[company])

                if len(orders) == 0:
                    api.get_position(company)
                    print(
                        "We hit the threshold to buy, but we already have some shares, so we won't buy more.")
            except Exception as e:
                api.submit_order(symbol=company, qty=shares,
                                 side="buy", type='market', time_in_force='gtc')
                print('We submitted the order to buy {} {} shares.'.format(
                    shares, company))

        elif trade_state == states.sell:
            try:
                api.get_position(company)
                api.submit_order(
                    symbol=company, qty=shares, side='sell', type='market', time_in_force='gtc')
                print('We submitted an order to sell {} {} shares.'.format(
                    shares, company))
            except:
                print(
                    "We hit the threshold to sell, but we don't have anything to sell. Next time maybe.")

        else:
            print("The RSI is {} and it's between the given thresholds: {} and {}, so we wait.".format(
                rsi_now, oversold_threshold, overbought_threshold))
    else:
        print("Not enough prices to calculate RSI and start trading:",
              len(data), "<=", rsi_timeframe)


print("I am ready to trade")
while True:
    market_is_open = api.get_clock().is_open
    if market_is_open:
        print("market_is_open")
        for company in companies:
            buyAndSell(company, days)
    else:
        print("Market is closed")

    print("I am waiting")
    time.sleep(60)
