from ensurepip import version
import config
from config import *
import alpaca_trade_api as tradeapi
import numpy as np
import time
import ast
import json
import talib as ta



API_KEY = config.API_KEY
SECRET_KEY = config.API_SECRET_KEY
BASE_URL = config.BASE_URL #base URL for paper trading
api = tradeapi.REST(key_id=API_KEY, secret_key=SECRET_KEY, base_url=BASE_URL) #For real trading, do not enter a base URL


rsi_timeframe = 14 #replace it with your prefered timeframe for RSI
oversold_threshold = 30 #replace it with your prefered oversold threshold 
overbought_threshold = 50 #replace it with your prefered overbought threshold
company = "AAPL" #"AAPL" #replace it with your prefered company symbol from: https://www.nyse.com/listings_directory/stock
shares = 1 #replace it with your prefered number of shares to buy/sell
data = [] #should be reseted every time you start the bot

pos_held = False

while True:
    print("")
    print("Checking Price for " + company)

    market_data = api.get_barset(company,'minute', limit=5) #Get one bar object for each of the past 5 minutes

    for bar in market_data[company]:
        data.append(bar.c)

    if len(data) > rsi_timeframe:
        np_data = np.array(data) # Convert to numpy array
        rsis = ta.RSI(np_data, rsi_timeframe)
        rsi_now = rsis[-1]

        if rsi_now < oversold_threshold:
            try:
                api.get_position(company)
                print("We hit the threshold to buy, but we already have some shares, so we won't buy more.")
            except:
                api.submit_order(symbol=company, qty=shares, side = "buy", type='market', time_in_force='gtc')
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

    time.sleep(60)





