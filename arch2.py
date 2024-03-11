import pandas as pd
import yfinance as yf
import numpy as np
import math
from ta.volatility import AverageTrueRange
from ta.momentum import RSIIndicator
import json

# Download historical data for desired ticker symbol
# sp500_stocks = ["AAPL"]
sp500_stocks = ["SPY", "AAPL", "MSFT", "AMZN", "JNJ", "XOM", "PG", "KO", "WMT", "INTC", "PFE", "DIS", "CSCO", "GE", "IBM", "GOOGL", "JPM", "V", "UNH", "HD", "MA", "VZ", "T", "PG", "CVX", "PEP", "WFC", "CMCSA", "COST", "BA", "MCD", "MDT", "ABT", "ORCL", "C", "KO", "MRK", "INTU", "ADBE", "AMGN", "TXN", "GILD", "QCOM", "MO", "MMM", "ACN", "GS", "SPG", "TGT", "USB", "SBUX", "CVS", "CAT"]


# ticker = 'AAPL'
res = []
res2 = []

for stock in sp500_stocks:

    data = yf.download(stock, start='2011-01-01', end='2021-01-01')

    investment = 100
    data['Daily_Returns'] = data['Close'].pct_change() + 1
    data['Synthetic_URO'] = investment * data['Daily_Returns'].cumprod()


    data['SMA_10'] = data['Synthetic_URO'].rolling(window=10).mean()
    data['SMA_30'] = data['Synthetic_URO'].rolling(window=30).mean()
    data['SMA_80'] = data['Synthetic_URO'].rolling(window=80).mean()
    data['SMA_100'] = data['Synthetic_URO'].rolling(window=100).mean()
    data['SMA_160'] = data['Synthetic_URO'].rolling(window=160).mean()

    data['Buy_Signal_10-30'] = (data['SMA_10'] > data['SMA_30']) & (data['SMA_10'].shift(1) < data['SMA_30'].shift(1))
    data['Sell_Signal_10-30'] = (data['SMA_10'] < data['SMA_30']) & (data['SMA_10'].shift(1) > data['SMA_30'].shift(1))

    data['Buy_Signal_30-100'] = (data['SMA_30'] > data['SMA_100']) & (data['SMA_30'].shift(1) < data['SMA_100'].shift(1))
    data['Sell_Signal_30-100'] = (data['SMA_30'] < data['SMA_100']) & (data['SMA_30'].shift(1) > data['SMA_100'].shift(1))

    data['Buy_Signal_80-160'] = (data['SMA_80'] > data['SMA_160']) & (data['SMA_80'].shift(1) < data['SMA_160'].shift(1))
    data['Sell_Signal_80-160'] = (data['SMA_80'] < data['SMA_160']) & (data['SMA_80'].shift(1) > data['SMA_160'].shift(1))

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

    # print(sharpe_ratio_1030)
    # print(sharpe_ratio_30100)
    # print(sharpe_ratio_80160)

    res.append([stock, sharpe_ratio_1030, sharpe_ratio_30100, sharpe_ratio_80160])


with open('list_data_simpleMA.json', 'w') as file:
    # Convert the list to JSON format and write it into the file
    json.dump(res, file)


