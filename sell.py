from helpers import oversold_threshold, overbought_threshold, checkToSell2

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


def sell(company):
    print("Checking Price for " + company)
    logfile.write(message_temp.format("Checking Price for " + company))

    sma_20 = fmp.get_sma(company, 20)
    price = fmp.get_price(company)

    print(sma_20, price)

    should_sell = checkToSell2(price, sma_20)


    def send_sell():
        return sms.send_sms("SELL " + company + " " + str(shares))

    if should_sell:
        sell_stock(company, logfile, send_sell, shares)

    else:
        print("We cannot sell {} at the moment.".format(company))
        logfile.write(message_temp.format(
            "We cannot sell {} at the moment.".format(company)))


print("I am ready to trade " + str(datetime.today()))
logfile.write(message_temp.format(
    "I am ready to trade " + str(datetime.today())))

market_is_open = get_is_market_open()


if market_is_open:
    print("market_is_open")
    logfile.write(message_temp.format("market_is_open"))
    screened_stocks = fmp.screen_stocks()
    for stock in companies:
        sell(stock)

else:
    print("Market is closed")
    logfile.write(message_temp.format("Market is closed"))

print("I am done")
logfile.write(message_temp.format("I am done" + "\n"))

logfile.close()
