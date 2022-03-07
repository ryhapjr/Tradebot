import config
from config import *
import alpaca_trade_api as tradeapi
import numpy as np
import time

API_KEY = config.API_KEY
SECRET_KEY = config.API_SECRET_KEY
BASE_URL = config.BASE_URL #base URL for paper trading
api = tradeapi.REST(key_id=API_KEY, secret_key=SECRET_KEY, base_url=BASE_URL) #For real trading, do not enter a base URL

symb = "SPY"
pos_held = False

while True:
    print("")
    print("Checking Price")

    market_data = api.get_barset(symb,'minute', limit=5) #Get one bar object for each of the past 5 minutes

    close_list = [] # This array will store all the closing prices from the last 5 minutes
    for bar in market_data[symb]:
        close_list.append(bar.c) #bar.c is the closing price of that bar's time interval

    close_list = np.array(close_list, dtype=np.float64) # Convert to numpy array
    ma = np.mean(close_list)
    last_price = close_list[4] #Most recent closing price

    print("Moving Average: " + str(ma))
    print("Last Price: " + str(last_price))

    if ma + 0.1 < last_price and not pos_held:
        print("Buy")
#Buy a stock

        api.submit_order(
            symbol='SPY',# Replace with a ticker of the stock you want to buy
            qty=1,
            side='buy',
            type='market',
            time_in_force='gtc' #Good 'til cancelled

    )
        pos_held = True
    elif ma - 0.1 > last_price and pos_held: # If MA is more than 10 cents above price, and we already bought
        print("Sell")
#Sell a stock
        api.submit_order(
            symbol='SPY',# Replace with a ticker of the stock you want to buy
            qty=1,
            side='sell',
            type='market',
            time_in_force='gtc' #Good 'til cancelled
        )
        pos_held = False

    time.sleep(60)





