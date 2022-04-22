from helpers import states, checkRSI, oversold_threshold, overbought_threshold

from alpaca import sell_stock, buy_stock, get_is_market_open

import time
import fmp
import sms
from datetime import datetime

logfile = open('log.txt', 'a+')
message_temp = '{}\n'

rsi_timeframe = 14  # replace it with your prefered timeframe for RSI

# company = "AAPL"  # "AAPL" #replace it with your prefered company symbol from: https://www.nyse.com/listings_directory/stock
shares = 1  # replace it with your prefered number of shares to buy/sell
data = []  # should be reseted every time you start the bot
days = 30  # replace it with your prefered number of days to calculate RSI


# list of stocks to trade on
companies = ['AAPL', 'GOOGL', 'GOOG', 'AMZN',
             'TSLA', 'FB', 'NVDA', 'TWTR', 'TSM', 'OKTA', 'MS']


def buyAndSell(company, days):
    print("Checking Price for " + company)
    logfile.write(message_temp.format("Checking Price for " + company))

    # ma = calculate_moving_average(company, 200)
    # ma_50 = calculate_moving_average(company, 50)
    # msc = calculate_macd(company, 60)

    # ma = fmp.get_ema(company)
    # ma_50 = fmp.get_ema(company)
    # print(ma, ma_50)
    # mast = checkMA(ma, ma_50)

    # market_data = fetch_data(company, days)
    # if market_data == None:
    #     print("No data for " + company)
    #     return

    # data = market_data.df['close']

    # if len(data) >= rsi_timeframe:
    # rsi_now = calculate_rsi(data, rsi_timeframe)
    rsi_data = fmp.get_rsi(company)
    rsi_now = rsi_data[0]['rsi']
    trade_state = checkRSI(rsi_now)

    print(rsi_now, trade_state)

    if trade_state == states.buy:
        buy_stock(company, logfile, shares, )
        sms.send_sms("BUY " + company + " " + str(shares))

    elif trade_state == states.sell:
        sell_stock(company, logfile, shares)
        sms.send_sms("SELL " + company + " " + str(shares))

    else:
        print("The RSI is {} and it's between the given thresholds: {} and {}, so we wait.".format(
            rsi_now, oversold_threshold, overbought_threshold))
        logfile.write(message_temp.format("The RSI is {} and it's between the given thresholds: {} and {}, so we wait.".format(
            rsi_now, oversold_threshold, overbought_threshold)))
    # else:
    #     print("Not enough prices to calculate RSI and start trading:",
    #           len(data), "<=", rsi_timeframe)


print("I am ready to trade " + str(datetime.today()))
logfile.write(message_temp.format(
    "I am ready to trade " + str(datetime.today())))

market_is_open = get_is_market_open()


if market_is_open:
    print("market_is_open")
    logfile.write(message_temp.format("market_is_open"))
    screened_stocks = fmp.screen_stocks()
    for stock in screened_stocks:
        buyAndSell(stock["symbol"], days)
else:
    print("Market is closed")
    logfile.write(message_temp.format("Market is closed"))

print("I am done")
logfile.write(message_temp.format("I am done" + "\n"))

logfile.close()
