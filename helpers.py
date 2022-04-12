from types import SimpleNamespace

states = SimpleNamespace(**{
    'buy': 'BUY',
    'sell': 'SELL',
    'hold': 'HOLD'
})


oversold_limit = 50
# replace it with your prefered oversold threshold - recommended > 30
oversold_threshold = 30
# replace it with your prefered overbought threshold -recommended < 70
overbought_threshold = 50


def checkRSI(rsi):
    if rsi > oversold_threshold and rsi < oversold_limit:
        return states.buy
    elif rsi > overbought_threshold:
        return states.sell
    else:
        return states.hold


def checkMA(ma, ma_50):
    if ma_50 > ma:  # golden cross
        return states.buy
    elif ma_50 < ma:  # death cross
        return states.sell
    else:
        return states.hold
