from DotW import stockUtils
import pandas_datareader.data as web
import datetime

def classify(row):
    if row['Adj Close'] > 0:
        return 'Up'
    return 'Down'

start = datetime.datetime(2014, 1, 1)
end = datetime.datetime.now()
print(end)
sp500 = stockUtils.get_constitutes('sp500')
print(sp500)
for ticker in sp500:
    symbol = ticker['symbol']
    prices = web.DataReader(symbol, 'yahoo', start, end)
    pct_change = prices.pct_change()
    pct_change = pct_change.ix[1:]
    pct_change['Up/Down'] = pct_change.apply(lambda x: classify(x),axis = 1)
    pct_change['Weekday'] = pct_change.index.map(lambda x: x.isoweekday())
    count = pct_change.groupby(['Weekday', 'Up/Down']).size()
    print(count)
    break

