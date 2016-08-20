from DotW import stockUtils
import pandas_datareader.data as web
import datetime

def classify(row):
    if row > 0:
        return 'Up'
    return 'Down'

start = datetime.datetime(2014, 1, 1)
end = datetime.datetime.now()
print(end)
sp500 = stockUtils.get_constitutes('sp500')
print(sp500)
for ticker in sp500:
    symbol = ticker['symbol']
    prices = web.DataReader(symbol, 'yahoo', start, end)['Adj Close']
    pct_change = prices.pct_change()
    pct_change = pct_change.ix[1:]
    pct_change['Up/Down'] = pct_change.apply(classify)
    print(pct_change)