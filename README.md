# Robo Advisors and Systematic Investing Final Project

## - Devansh Purohit

### Introduction

Two trading strategies have been presented: the first being a Combination of Moving Averages and Counter Trend Systems, and the other introducing the RSI (Relative Strength Index) Indicator and AverageTrueRange to take advantage of momentum in the market while also accounting for market volatility. Python code was used to implement these strategies and stock data was imported from Yahoo! Finance.

...

### Appendix A

Code for RSI/ATR Strategy:

```python
import pandas as pd
import yfinance as yf
import numpy as np
import math
from ta.volatility import AverageTrueRange
from ta.momentum import RSIIndicator
import json

# Download historical data for desired ticker symbol
sp500_stocks = ["SPY", "AAPL", "MSFT", "AMZN", "JNJ", "XOM", "PG", "KO", "WMT", "INTC", "PFE", "DIS", "CSCO", "GE", "IBM", "GOOGL", "JPM", "V", "UNH", "HD", "MA", "VZ", "T", "PG", "CVX", "PEP", "WFC", "CMCSA", "COST", "BA", "MCD", "MDT", "ABT", "ORCL", "C", "KO", "MRK", "INTU", "ADBE", "AMGN", "TXN", "GILD", "QCOM", "MO", "MMM", "ACN", "GS", "SPG", "TGT", "USB", "SBUX", "CVS", "CAT"]
...

```

(Note: The above content is a sample and truncated version of the actual content for demonstration. The actual markdown file would contain the complete content as presented in the PDF.)
