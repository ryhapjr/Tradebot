from alpaca_trade_api.rest import REST, TimeFrame
import config
# import talib as ta
from datetime import datetime, timedelta
# import numpy as np

API_KEY = config.API_KEY
SECRET_KEY = config.API_SECRET_KEY
BASE_URL = config.BASE_URL  # base URL for paper trading

api = REST(key_id=API_KEY, secret_key=SECRET_KEY, base_url=BASE_URL)

api_time_format = '%Y-%m-%d'


def calculate_start_end(days):
    now = datetime.now()
    start_time = (now.date() -
                  timedelta(days=days))
    end_time = (now.date() -
                timedelta(days=1)).strftime(api_time_format)
    return start_time, end_time


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


def get_is_market_open():
    return api.get_clock().is_open


def buy_stock(company, shares=1):
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


def sell_stock(company, shares=1):
    try:
        api.get_position(company)
        api.submit_order(
            symbol=company, qty=shares, side='sell', type='market', time_in_force='gtc')
        print('We submitted an order to sell {} {} shares.'.format(
            shares, company))
    except:
        print(
            "We hit the threshold to sell, but we don't have anything to sell. Next time maybe.")


# def calculate_moving_average(company, days):
#     try:
#         market_data = fetch_data(company, days * 2)
#         if market_data == None:
#             return 0
#         close_prices = np.array(market_data.df['close'])
#         sma = ta.SMA(close_prices, days)[-1]
#         return sma
#     except Exception as e:
#         print(e)
#         return 0


# def calculate_rsi(data, timeframe):
#     np_data = np.array(data)  # Convert to numpy array
#     rsis = ta.RSI(np_data, timeframe)
#     return rsis[-1]


# def calculate_macd(company, days):
#     try:
#         market_data = fetch_data(company, days)
#         if market_data == None:
#             return 0
#         close_prices = np.array(market_data.df['close'])

#         macd, macdsignal, macdhist = ta.MACD(
#             close_prices, fastperiod=12, slowperiod=26, signalperiod=9)
#         # print(macd[-1])
#         # print(macdsignal[-1])
#         # print(macdhist[-1])
#         return macdhist[-1]

#     except Exception as e:
#         print(e)
#         return 0
