from helpers import oversold_threshold, overbought_threshold, checkToBuy2

from alpaca import sell_stock, buy_stock, get_is_market_open

import aac
import fmp
import sms
from datetime import datetime

logfile = open('log.txt', 'a+')
message_temp = '{}\n'

shares = 1  # replace it with your prefered number of shares to buy/sell


# list of stocks to trade on
# companies = ['AAPL', 'GOOGL', 'GOOG', 'AMZN',
#              'TSLA', 'FB', 'NVDA', 'TWTR', 'TSM', 'OKTA', 'MS']  # from: https://www.nyse.com/listings_directory/stock

companies = ['AAPL', 'NVDA', 'TSLA', 'LLY', 'XOM', 'UPST']
# UPST


def buy(company):
    print("Checking Price for " + company)
    logfile.write(message_temp.format("Checking Price for " + company))


    ema_21 = fmp.get_ema(company, 21)
    sma_10 = fmp.get_sma(company, 10)
    rsi = fmp.get_rsi(company)
    price = fmp.get_price(company)

    print(ema_21, sma_10,sma_20, price)

    should_buy = checkToBuy2(ema_21, sma_10, rsi, price)


    def send_buy():
        return sms.send_sms("BUY " + company + " " + str(shares))

    if should_buy:
        buy_stock(company, logfile, send_buy, shares)

    else:
        print("We cannot buy or sell {} at the moment.".format(company))
        logfile.write(message_temp.format(
            "We cannot buy or sell {} at the moment.".format(company)))


print("I am ready to trade " + str(datetime.today()))
logfile.write(message_temp.format(
    "I am ready to trade " + str(datetime.today())))

market_is_open = get_is_market_open()


if market_is_open:
    print("market_is_open")
    logfile.write(message_temp.format("market_is_open"))
    screened_stocks = fmp.screen_stocks()
    for stock in companies:
        buy(stock)
    # if screened_stocks == None:
    #     print("No stocks to trade")
    #     logfile.write(message_temp.format("No stocks to trade"))
    # else:
    #     for stock in screened_stocks:
    #         buyAndSell(stock["symbol"])

else:
    print("Market is closed")
    logfile.write(message_temp.format("Market is closed"))

print("I am done")
logfile.write(message_temp.format("I am done" + "\n"))

logfile.close()
