import pandas as pd
import numpy as np
import math

# Assuming 'data' is your DataFrame and it includes 'Close' prices.
data = pd.read_csv('uro.csv')


investment = 100
data['Daily_Returns'] = data['Close'].pct_change() + 1
data['Synthetic_URO'] = investment * data['Daily_Returns'].cumprod()

data['SMA_10'] = data['Synthetic_URO'].rolling(window=10).mean()
data['SMA_30'] = data['Synthetic_URO'].rolling(window=30).mean()
data['SMA_80'] = data['Synthetic_URO'].rolling(window=80).mean()
data['SMA_100'] = data['Synthetic_URO'].rolling(window=100).mean()
data['SMA_160'] = data['Synthetic_URO'].rolling(window=160).mean()



# Calculate z-score of the last 20 days
data['z_score'] = (data['Close'] - data['Close'].rolling(window=30).mean()) / data['Close'].rolling(window=30).std(ddof=0)

# Create signals
data['Buy_Signal_10-30'] = (data['SMA_10'] > data['SMA_30']) & (data['z_score'] > -1)
data['Sell_Signal_10-30'] = (data['SMA_10'] < data['SMA_30']) & (data['z_score'] < 1)

data['Buy_Signal_30-100'] = (data['SMA_30'] > data['SMA_100']) & (data['z_score'] > -1)
data['Sell_Signal_30-100'] = (data['SMA_30'] < data['SMA_100']) & (data['z_score'] < 1)

data['Buy_Signal_80-160'] = (data['SMA_80'] > data['SMA_160']) & (data['z_score'] > -1)
data['Sell_Signal_80-160'] = (data['SMA_80'] < data['SMA_160']) & (data['z_score'] < 1)

# Create a column 'Position' where we are long (+1) when Buy_Signal is True, short (-1) when Sell_Signal is True, and flat (0) otherwise
data['Position_10-30'] = np.where(data['Sell_Signal_10-30'], -1, np.where(data['Buy_Signal_10-30'], 1, 0))
data['Position_30-100'] = np.where(data['Sell_Signal_30-100'], -1, np.where(data['Buy_Signal_30-100'], 1, 0))
data['Position_80-160'] = np.where(data['Sell_Signal_80-160'], -1, np.where(data['Buy_Signal_80-160'], 1, 0))

# Forward fill our Position column to simulate holding our position
data['Position_10-30'] = data['Position_10-30'].ffill()
data['Position_30-100'] = data['Position_30-100'].ffill()
data['Position_80-160'] = data['Position_80-160'].ffill()

# Calculate daily returns of strategy
data['Strategy_Returns_10-30'] = data['Close'].pct_change() * data['Position_10-30'] 
data['Strategy_Returns_10-30'] = data['Strategy_Returns_10-30'] * 100

data['Strategy_Returns_30-100'] = data['Close'].pct_change() * data['Position_30-100'] 
data['Strategy_Returns_30-100'] = data['Strategy_Returns_30-100'] * 100

data['Strategy_Returns_80-160'] = data['Close'].pct_change() * data['Position_80-160'] 
data['Strategy_Returns_80-160'] = data['Strategy_Returns_80-160'] * 100

# Calculate Sharpe Ratio
excess_returns = data['Strategy_Returns_10-30']
sharpe_ratio_1030 = math.sqrt(260) * excess_returns.mean() / excess_returns.std()

excess_returns = data['Strategy_Returns_30-100']
sharpe_ratio_30100 = math.sqrt(260) * excess_returns.mean() / excess_returns.std()

excess_returns = data['Strategy_Returns_80-160']
sharpe_ratio_80160 = math.sqrt(260) * excess_returns.mean() / excess_returns.std()

print(sharpe_ratio_1030)
print(sharpe_ratio_30100)
print(sharpe_ratio_80160)