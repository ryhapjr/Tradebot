from helpers import oversold_threshold, overbought_threshold, checkToBuy, checkToSell

from alpaca import sell_stock, buy_stock, get_is_market_open

import aac
import fmp
import sms
from datetime import datetime

logfile = open('log.txt', 'a+')
message_temp = '{}\n'

shares = 1  # replace it with your prefered number of shares to buy/sell


# list of stocks to trade on
companies = ['AAPL', 'GOOGL', 'GOOG', 'AMZN',
             'TSLA', 'FB', 'NVDA', 'TWTR', 'TSM', 'OKTA', 'MS']  # from: https://www.nyse.com/listings_directory/stock


def buyAndSell(company):
    print("Checking Price for " + company)
    logfile.write(message_temp.format("Checking Price for " + company))

    ema_21 = fmp.get_ema(company, 21)
    sma_20 = fmp.get_sma(company, 20)
    sma_50 = fmp.get_sma(company, 50)
    sma_100 = fmp.get_sma(company, 100)
    sma_200 = fmp.get_sma(company, 200)
    rsi = fmp.get_rsi(company)
    macd = aac.get_macd(company)
    price = fmp.get_price(company)
    print(ema_21, sma_20, sma_50,
          sma_100, sma_200, rsi, macd, price)

    should_buy = checkToBuy(ema_21, sma_20, sma_50,
                            sma_100, sma_200, rsi, macd)

    should_sell = checkToSell(price, sma_50)

    def send_buy():
        return sms.send_sms("BUY " + company + " " + str(shares))

    def send_sell():
        return sms.send_sms("SELL " + company + " " + str(shares))

    if should_buy:
        buy_stock(company, logfile, send_buy, shares)

    elif should_sell:
        sell_stock(company, logfile, send_sell, shares)

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
    # for stock in companies:
    #     buyAndSell(stock)
    if screened_stocks == None:
        print("No stocks to trade")
        logfile.write(message_temp.format("No stocks to trade"))
    else:
        for stock in screened_stocks:
            buyAndSell(stock["symbol"])

else:
    print("Market is closed")
    logfile.write(message_temp.format("Market is closed"))

print("I am done")
logfile.write(message_temp.format("I am done" + "\n"))

logfile.close()
