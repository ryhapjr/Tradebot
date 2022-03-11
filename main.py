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


API_KEY = config.API_KEY
SECRET_KEY = config.API_SECRET_KEY
BASE_URL = config.BASE_URL #base URL for paper trading
api = REST(key_id=API_KEY, secret_key=SECRET_KEY, base_url=BASE_URL) #For real trading, do not enter a base URL


rsi_timeframe = 14 #replace it with your prefered timeframe for RSI
oversold_limit = 50
oversold_threshold = 30 #replace it with your prefered oversold threshold - recommended > 30
overbought_threshold = 50 #replace it with your prefered overbought threshold -recommended < 70
company = "AAPL" #"AAPL" #replace it with your prefered company symbol from: https://www.nyse.com/listings_directory/stock
shares = 1 #replace it with your prefered number of shares to buy/sell
data = [] #should be reseted every time you start the bot
days = 30 #replace it with your prefered number of days to calculate RSI
api_time_format = '%Y-%m-%d'#T%H:%M:%S.%f-04:00' # API datetimes will match this format. (-04:00 represents the market's TZ.)


pos_held = False

while True:
    market_is_open = api.get_clock().is_open
    if market_is_open:
        print("")
        print("Checking Price for " + company)
        now = datetime.now()
        start_time = (now.date() -
                        timedelta(days=days))
        end_time = now.strftime(api_time_format)

   
        print(start_time)
        print(end_time)


        market_data = api.get_bars(company,TimeFrame.Day, start_time, end_time)
        print(market_data)

        temp = []
        for bar in market_data:
            temp.append(bar.c)

        data = temp
        if len(data) >= rsi_timeframe:
            np_data = np.array(data) # Convert to numpy array
            rsis = ta.RSI(np_data, rsi_timeframe)
            rsi_now = rsis[-1]

            print(rsi_now)

            if rsi_now > oversold_threshold and rsi_now < oversold_limit:
                try:
                    orders = api.list_orders(symbols=[company])

                    if len(orders) == 0:
                        api.get_position(company)
                        print("We hit the threshold to buy, but we already have some shares, so we won't buy more.")
                except Exception as e:
                    print("error")
                    print(e)
                    api.submit_order(symbol=company, qty=shares, side="buy", type='market', time_in_force='gtc')
                    print('We submitted the order to buy {} {} shares.'.format(shares, company))
                
            elif rsi_now > overbought_threshold:
                try:
                    api.get_position(company)
                    api.submit_order(symbol=company,qty=shares,side='sell',type='market',time_in_force='gtc')
                    print('We submitted an order to sell {} {} shares.'.format(shares, company))
                except:
                    print("We hit the threshold to sell, but we don't have anything to sell. Next time maybe.")
            
            else:
                print("The RSI is {} and it's between the given thresholds: {} and {}, so we wait.".format(rsi_now, oversold_threshold, overbought_threshold))
        else:
            print("Not enough prices to calculate RSI and start trading:", len(data), "<=", rsi_timeframe)
    else:
        print("Market is closed")

    time.sleep(60)





