import pandas as pd
import numpy as np
import math
from ta.volatility import AverageTrueRange
from ta.momentum import RSIIndicator



# Assuming 'data' is your DataFrame and it includes 'Close' prices.
data = pd.read_csv('uro.csv')

# Calculate RSI
data['RSI'] = RSIIndicator(data['Close']).rsi()

investment = 100
data['Daily_Returns'] = data['Close'].pct_change() + 1
data['Synthetic_URO'] = investment * data['Daily_Returns'].cumprod()


# Calculate ATR
data['ATR'] = AverageTrueRange(data['High'], data['Low'], data['Close']).average_true_range()

# Sell when RSI crosses below 70 (overbought) and ATR is high (volatility is high)
data['Buy_Signal_7030'] = (data['RSI'] > 30) & (data['RSI'].shift(1) <= 30) & (data['ATR'] > data['ATR'].mean())
data['Sell_Signal_7030'] = (data['RSI'] < 70) & (data['RSI'].shift(1) >= 70) & (data['ATR'] > data['ATR'].mean())


data['Buy_Signal_8020'] = (data['RSI'] > 20) & (data['RSI'].shift(1) <= 20) & (data['ATR'] > data['ATR'].mean())
data['Sell_Signal_8020'] = (data['RSI'] < 80) & (data['RSI'].shift(1) >= 80) & (data['ATR'] > data['ATR'].mean())


data['Buy_Signal_6040'] = (data['RSI'] > 40) & (data['RSI'].shift(1) <= 40) & (data['ATR'] > data['ATR'].mean())
data['Sell_Signal_6040'] = (data['RSI'] < 60) & (data['RSI'].shift(1) >= 60) & (data['ATR'] > data['ATR'].mean())


data['Position_70-30'] = np.where(data['Sell_Signal_7030'], -1, np.where(data['Buy_Signal_7030'], 1, 0))
data['Position_80-20'] = np.where(data['Sell_Signal_8020'], -1, np.where(data['Buy_Signal_8020'], 1, 0))
data['Position_60-40'] = np.where(data['Sell_Signal_6040'], -1, np.where(data['Buy_Signal_6040'], 1, 0))

# Forward fill our Position column to simulate holding our position
data['Position_70-30'] = data['Position_70-30'].ffill()
data['Position_80-20'] = data['Position_80-20'].ffill()
data['Position_60-40'] = data['Position_60-40'].ffill()

# Calculate daily returns of strategy
data['Strategy_Returns_70-30'] = data['Close'].pct_change() * data['Position_70-30'] 
data['Strategy_Returns_70-30'] = data['Strategy_Returns_70-30'] * 100

data['Strategy_Returns_80-20'] = data['Close'].pct_change() * data['Position_80-20'] 
data['Strategy_Returns_80-20'] = data['Strategy_Returns_80-20'] * 100

data['Strategy_Returns_60-40'] = data['Close'].pct_change() * data['Position_60-40'] 
data['Strategy_Returns_60-40'] = data['Strategy_Returns_60-40'] * 100

# Calculate Sharpe Ratio
excess_returns = data['Strategy_Returns_70-30']
sharpe_ratio_7030 = math.sqrt(260) * excess_returns.mean() / excess_returns.std()

excess_returns = data['Strategy_Returns_80-20']
sharpe_ratio_8020 = math.sqrt(260) * excess_returns.mean() / excess_returns.std()

excess_returns = data['Strategy_Returns_60-40']
sharpe_ratio_9010 = math.sqrt(260) * excess_returns.mean() / excess_returns.std()

print(sharpe_ratio_7030)
print(sharpe_ratio_8020)
print(sharpe_ratio_9010)
