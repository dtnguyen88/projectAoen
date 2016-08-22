from DotW import stockUtils
import pandas_datareader.data as web
import datetime
import scipy.stats as stats


def classify(row):
    if row['Adj Close'] > 0:
        return 'Up'
    return 'Down'


def binomial_up_down_test(up, down, crit):
    if up >= down:
        direction = 'Up'
        pvalue = stats.binom_test(up, up + down, 0.5)
    else:
        direction = 'Down'
        pvalue = stats.binom_test(down, up + down, 0.5)
    if pvalue <= crit:
        return {'direction':direction, 'pvalue':pvalue}
    return {}

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
    for i in range(5):
        up = count[i+1]['Up']
        down = count[i+1]['Down']
        test = binomial_up_down_test(up, down, 0.01)
        if len(test):
            print("Found stock: "+ symbol+ " is biased in directon: " + test['direction'] + " at date: " + str(i+1) + " and p-value as: " + str(test['pvalue']))