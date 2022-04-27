from helpers import states, checkRSI, oversold_threshold, overbought_threshold, checKMACD, checkATR, checkMA

from alpaca import sell_stock, buy_stock, get_is_market_open

import aac
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


def buyAndSell(company):
    print("Checking Price for " + company)
    logfile.write(message_temp.format("Checking Price for " + company))

    ma_200 = fmp.get_sma(company, 200)
    ma_50 = fmp.get_sma(company, 50)
    print('ma_200: ' + str(ma_200))
    print('ma_50: ' + str(ma_50))
    ma_state = checkMA(ma_50, ma_200)
    print('ma_state: ' + str(ma_state))

    atr = aac.get_atr(company)
    print('atr: ' + str(atr))
    atr_state = checkATR(atr, ma_50)
    print('atr_state: ' + str(atr_state))

    rsi = fmp.get_rsi(company)
    print('rsi: ' + str(rsi))
    rsi_state = checkRSI(rsi)
    print('rsi_state: ' + str(rsi_state))

    if rsi_state == states.buy:
        buy_stock(company, logfile, shares, )
        sms.send_sms("BUY " + company + " " + str(shares))

    elif rsi_state == states.sell:
        sell_stock(company, logfile, shares)
        sms.send_sms("SELL " + company + " " + str(shares))

    else:
        print("The RSI is {} and it's between the given thresholds: {} and {}, so we wait.".format(
            rsi, oversold_threshold, overbought_threshold))
        logfile.write(message_temp.format("The RSI is {} and it's between the given thresholds: {} and {}, so we wait.".format(
            rsi, oversold_threshold, overbought_threshold)))
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
    # for stock in companies:
    #     buyAndSell(stock)
    if screened_stocks == None:
        print("No stocks to trade")
        logfile.write(message_temp.format("No stocks to trade"))
    else:
        for stock in screened_stocks:
            buyAndSell(stock["symbol"], days)

else:
    print("Market is closed")
    logfile.write(message_temp.format("Market is closed"))

print("I am done")
logfile.write(message_temp.format("I am done" + "\n"))

logfile.close()
