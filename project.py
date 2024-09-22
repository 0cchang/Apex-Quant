import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np

### data pipeline
forex_data = yf.download('EURUSD=X', start='2024-3-01', end='2024-9-01') # get data
forex_data.index = pd.to_datetime(forex_data.index)

forex_data.drop(columns = ['Adj Close','Volume'], inplace = True) # drop unneeded columns

forex_data.interpolate() # handle missing data by interpolating

### basic strategy
rows = forex_data.shape[0]
longTotal = 0
shortTotal = 0

portfolio = 100000.0 # measured in euros

trades = winningTrades = 0

profit = []
equity = []

shortPrice = -1
longPrice = -1
for i in range(rows-1):
    currentClose = forex_data.iloc[i]['Close']
    
    currProfit = 0
    if shortPrice != -1: # calculate profit from shorting, im assuming we are closing daily
        currProfit = (shortPrice - currentClose) * portfolio * 0.05
        
    if longPrice != -1:
        currProfit = (currentClose - longPrice) * portfolio * 0.05

    if currProfit > 0:
        winningTrades += 1
    profit.append(currProfit)
    equity.append(currProfit + portfolio)
    portfolio += currProfit

    longTotal += currentClose
    shortTotal += currentClose

    if i > 50: #50 days longMA
        longTotal -= forex_data.iloc[i-50]['Close']

    if i > 20: #20 days shortMA
        shortTotal -= forex_data.iloc[i-20]['Close']
    
    
    if i > 50:
        currentOpen = forex_data.iloc[i]['Open']
        trades += 1
        if (longTotal / 50 - shortTotal / 20) > 0:  #longMA more than shortMA, short on EURO 
            shortPrice = currentOpen 
            longPrice = -1
        else: #else long on EURO
            longPrice = currentOpen
            shortPrice = -1
            

##summary plot

print("total profit: ", sum(profit))
print("trades: ", trades)
print("winning trades %: ", (winningTrades / trades) * 100)

treasuryNote10 = 0.025
returns = np.array(profit)

risk_free_rate = 0.025 # us treasury return

mean_return = np.mean(returns)
std_dev = np.std(returns)

sharpe_ratio = (mean_return - risk_free_rate) / std_dev

print("Sharpe Ratio: ",sharpe_ratio)

xs = [x for x in range(len(equity))]

plt.plot(xs, equity)
plt.show()

plt.close()
