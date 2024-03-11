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

    # Calculate RSI
    data['RSI'] = RSIIndicator(data['Close']).rsi()

    investment = 100
    data['Daily_Returns'] = data['Close'].pct_change() + 1
    data['Synthetic_URO'] = investment * data['Daily_Returns'].cumprod()

    # Calculate ATR
    data['ATR'] = AverageTrueRange(data['High'], data['Low'], data['Close']).average_true_range()

    data['Buy_Signal_7030'] = (data['RSI'] > 30) & (data['RSI'].shift(1) <= 30) & (data['ATR'] > data['ATR'].mean())
    data['Sell_Signal_7030'] = (data['RSI'] < 70) & (data['RSI'].shift(1) >= 70) & (data['ATR'] > data['ATR'].mean())

    data['Buy_Signal_8020'] = (data['RSI'] > 20) & (data['RSI'].shift(1) <= 20) & (data['ATR'] > data['ATR'].mean())
    data['Sell_Signal_8020'] = (data['RSI'] < 80) & (data['RSI'].shift(1) >= 80) & (data['ATR'] > data['ATR'].mean())


    data['Buy_Signal_6040'] = (data['RSI'] > 40) & (data['RSI'].shift(1) <= 40) & (data['ATR'] > data['ATR'].mean())
    data['Sell_Signal_6040'] = (data['RSI'] < 60) & (data['RSI'].shift(1) >= 60) & (data['ATR'] > data['ATR'].mean())


    data['Position_70-30'] = np.where(data['Sell_Signal_7030'], -1, np.where(data['Buy_Signal_7030'], 1, 0))
    data['Position_70-30'] = data['Position_70-30'].ffill()

    data['Position_80-20'] = np.where(data['Sell_Signal_8020'], -1, np.where(data['Buy_Signal_8020'], 1, 0))
    data['Position_60-40'] = np.where(data['Sell_Signal_6040'], -1, np.where(data['Buy_Signal_6040'], 1, 0))
    data['Position_80-20'] = data['Position_80-20'].ffill()
    data['Position_60-40'] = data['Position_60-40'].ffill()



    data['Strategy_Returns_70-30'] = data['Close'].pct_change() * data['Position_70-30'] 
    data['Strategy_Returns_70-30'] = data['Strategy_Returns_70-30'] * 100

    data['Strategy_Returns_80-20'] = data['Close'].pct_change() * data['Position_80-20'] 
    data['Strategy_Returns_80-20'] = data['Strategy_Returns_80-20'] * 100

    data['Strategy_Returns_60-40'] = data['Close'].pct_change() * data['Position_60-40'] 
    data['Strategy_Returns_60-40'] = data['Strategy_Returns_60-40'] * 100

    excess_returns = data['Strategy_Returns_70-30']
    sharpe_ratio_7030 = math.sqrt(260) * excess_returns.mean() / excess_returns.std()

    excess_returns = data['Strategy_Returns_80-20']
    sharpe_ratio_8020 = math.sqrt(260) * excess_returns.mean() / excess_returns.std()

    excess_returns = data['Strategy_Returns_60-40']
    sharpe_ratio_6040 = math.sqrt(260) * excess_returns.mean() / excess_returns.std()

    res.append([stock, sharpe_ratio_7030, sharpe_ratio_6040, sharpe_ratio_8020])


with open('list_data_RSI_ATR.json', 'w') as file:
    # Convert the list to JSON format and write it into the file
    json.dump(res, file)


