1. Moving average should be on uptrend after 200 days from starting point from 1st day

2. The bot being able to pick stocks that fit our criteria without me doing the work for it ? Another bot ?

3. Database , codesphere , will I have to keep this running on my computer daily ?

MACD
fast ema period 12
slow ema period 26
sign line period 9

#strategy 1

```
Scalping Strategy:
  Get Tradeable Stocks
    Filter for Recent News
    Filter for Volatile Stocks
    Filter for Trending Stocks
  Sort by Trendrate
  Itereate Through Filtered Stocks
    Buy Limit Order
    Sell Limit Order
```

```
Trading Algo PScode:
    initialize tradeable stocks list
    Iterate through list of stocks:
        if stock is tradeable
        AND if stock's most recent news is positive
        AND if stock most recent news has been posted in last 30 minutes:
        AND stock volume < avg. volume:
            add stock ticker and number of clicks to tradeable stock list
    sort tradeable stocks list by number of clicks
    for each stock ticker:
        calculate 20 minute moving average
            stocks_price_day = rs.stocks.get_historicals(inputSymbols='tsla', span='day')
            get last 4 open prices and divide by 4 = 20 minute moving average
        #see if stock is trending upwards
        if 20 minute moving average > current_price:
            #place buy-limit order to buy at the current price
            robin_stocks.orders.order_buy_limit(symbol, quantity, limitPrice, timeInForce='gtc', extendedHours=False)
```

https://towardsdatascience.com/how-to-get-started-building-a-stock-cryptocurrency-forex-trading-program-2abbf0a4729f

https://medium.com/analytics-vidhya/stream-stock-data-6bac816ca6d0

https://arshyasharifian.medium.com/real-time-bitcoin-price-streaming-using-oracle-cloud-services-2f3fcb3adfb2

http://francescopochetti.com/scrapying-around-web/

https://medium.com/automation-generation/concurrent-scalping-algo-using-async-python-8df9f31e22f1

https://towardsdatascience.com/options-trading-technical-analysis-using-python-f403ec2985b4

https://towardsdatascience.com/get-up-to-date-financial-ratios-p-e-p-b-and-more-of-stocks-using-python-4b53dd82908f

https://medium.com/swlh/400-trading-algorithms-later-bc76279bc525

https://medium.com/swlh/coding-your-way-to-wall-street-bf21a500376f

https://ai.plainenglish.io/stock-day-trading-bot-2f0ecc6e581a

https://www.investopedia.com/articles/active-trading/081315/how-code-your-own-algo-trading-robot.asp

https://www.devteam.space/blog/how-to-build-a-crypto-trading-bot/

https://www.trality.com/blog/build-python-trading-bot

https://yakkomajuri.medium.com/a-step-by-step-guide-to-building-a-trading-bot-in-any-programming-language-d202ffe91569

https://medium.com/swlh/build-an-ai-stock-trading-bot-for-free-4a46bec2a18

https://www.codementor.io/@powderblock/algo-trading-101-building-your-first-stock-trading-bot-in-python-13fwsexn5f

https://www.activestate.com/blog/how-to-build-an-algorithmic-trading-bot/

https://www.trality.com/blog/create-binance-trading-bot

https://alpaca.markets/learn/how-to-build-a-trading-bot-with-alpaca-and-trellis/

https://www.trellistrade.co/setup-bot/packs

https://github.com/alpacahq/alpaca-trade-api-python/

https://github.com/alpacahq/alpaca-trade-api-python/blob/master/examples/long-short.py

https://superai.pl/the_simple_trading_bot_2.html

https://superai.pl/the_simple_trading_bot_3.html

https://github.com/alpacahq/alpaca-trade-api-python/blob/d560c9b2278fdcf17a0687c14b1f33ab2aa2dc11/examples/overnight_hold.py#L111

https://github.com/alpacahq/alpaca-trade-api-python/blob/master/examples/historic_async.py

https://github.com/alpacahq/alpaca-trade-api-python/blob/master/examples/martingale.py

https://github.com/alpacahq/alpaca-trade-api-python/blob/master/examples/websockets/v2_example.py

https://github.com/PythonForForex/Alpaca-Trading-API-Guide-A-Step-by-step-Guide/blob/master/Alpaca_examples.py
