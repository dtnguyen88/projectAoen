"""
MONTE CARLO PLAIN VANILLA OPTION PRICING
This script is used to estimate the price of a plain vanilla
option using the Monte Carlo method and assuming that returns
can be simulated using an estimated probability density (KDE estimate)
Call option quotations are available at:
http://www.google.com/finance/option_chain?q=NASDAQ%3AAAPL&ei=fNHBVaicDsbtsAHa7K-QDQ
Risk free* rates can be found here:
http://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=yield
In this script the following assumptions are made:
- Returns are not exactly normally distributed, but they following
a historical distribution that can be estimated from the historical prices.
Therefore, the price of the stock at time t+1
can be assumed to be:
s1 = s0 + s0*K
where: t=1 and K is a random variable whose density is described by the
empirical estimated density of the actual stock returns.
*I choose these as risk free (even though they are not), the concept of
risk free may be subjective.
"""

import pickle
import numpy as np

# Load the estimated probability density
pickle_in = open("KDE_","rb")
kde_dist = pickle.load(pickle_in)
pickle_in.close()

# Check that the total area under the probability density sums up to 1
print("Area below the curve from -10 to 10:",kde_dist.integrate_box(-10,10),'\n')

# Optional seed
#np.random.seed(12345678)

# Stocastic walk
# This function calculates the simulated price after periods
# and returns the final price.
def stoc_walk(p,periods):
    w = kde_dist.resample(size=periods)[0]		#compare to parametric: w = np.random.normal(0,1,size=periods)
    for i in range(periods):
        p += p*w[i] 						#compare to parametric: p += dr*p + w[i]*vol*p
    return p

# Parameters
s0 = 230.03		# Actual price
t_ = 365		# Total periods in a year
r = 0.0019    	# Risk free rate (yearly)
days = 14		# Days until option expiration
N = 100000		# Number of Monte Carlo trials
zero_trials = 0		# Number of trials where the option payoff = 0
k=220			# Strike price

avg = 0			# Temporary variable to be assigned to the sum
			# of the simulated payoffs

# Simulation loop
for i in range(N):
    temp = stoc_walk(s0,days)
    if temp < k:
        payoff = k- temp
        payoff = payoff*np.exp(-r/t_*days)
        avg += payoff
    else:
        zero_trials += 1

# Averaging the payoffs
price = avg/float(N)

# Priting the results
print("MONTE CARLO PLAIN VANILLA PUT OPTION PRICING")
print("Option price: ",price)
print("Initial price: ",s0)
print("Strike price: ",k)
print("Total trials: ",N)
print("Zero trials: ",zero_trials)
print("Percentage of total trials: ",zero_trials/N*100,"%")
