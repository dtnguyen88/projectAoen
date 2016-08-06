"""
Auxiliary script:
This script is used to open the .csv file containing the
closing prices, calculating the percentage changes for 
each couple of days and then output the data as a new .csv
file.

Optionally we can plot the data to take a look at what has
been generated.

"""
import matplotlib.pyplot as plt
import pandas as pd
import pandas.io.data as web
import os
import datetime
start = datetime.datetime(2014,1,1)
end = datetime.datetime.today()

# Read original .csv with pandas
file = web.DataReader("TSLA", 'google', start, end)

# Select only closing prices
close_price = file['Close']

# Calculate percentage changes
pc = close_price.pct_change()

# Output .csv file
pc.to_csv('pc.csv')

# Optional plot of the data
plt.plot(pc[:])
plt.show()
