"""
AAPL summary

Given the file with percentage changes,
this script is used to calculate the following:
- Estimated average price changes
- Estimated standard deviation
- Kurtosis of the empirical data
- Skew of the empirical data
- Estimated probability density of percentage changes

The empirical probability density is estimated using 
gaussian_kde from the scipy stats.

Using matplotlib.pyplot the estimated density is compared
to the parametric density and the histograms of percentage
changes is plotted.

Finally, the kde object is stored using pickle.

"""

import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.stats.kde import gaussian_kde
import numpy as np
import pandas as pd
import pickle

import matplotlib.pyplot as plt
import pandas.io.data as web
import os
import datetime
start = datetime.datetime(2015,1,1)
end = datetime.datetime.today()

# Read original .csv with pandas
file = web.DataReader("TSLA", 'google', start, end)

# Select only closing prices
close_price = file['Close']

# Calculate percentage changes
pc = close_price.pct_change()
pc =pc.dropna()
print(pc)
# Calculate avg and stdv
daily_ret = pc.mean()
daily_std = pc.std()
k = pc.kurtosis()
s = pc.skew()

# Print out results
print("Stock TSLA")
print("Daily Return (historical average): ",daily_ret*100,"%")
print("Daily Standard Deviation (historical average): ",daily_std*100,"%")
print("Kurtosis: ",k)
print("Skew: ",s)

# Estimate the probability density using KDE
KDEpdf = gaussian_kde(pc[:])

# Plotting variables and plot
x = np.linspace(-1.5,1.5,1500)
ymax = pc.max()
ymin = pc.min()
step = 0.005

plt.plot(x,KDEpdf(x),'blue',label='KDE estimated distribution')
plt.hist(pc[:],normed=1,color='cyan',bins=np.linspace(ymin,ymax,(ymax-ymin/step)))
plt.plot(x,norm.pdf(x,daily_ret,daily_std),color='red',label='Parametric dist')
plt.legend()
plt.show()

# Save KDE object
pickle_out = open("KDE_","wb")
pickle.dump(KDEpdf,pickle_out)
pickle_out.close()