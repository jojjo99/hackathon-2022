#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 20:11:50 2022

@author: johanna
"""
import sys
#sys.path.append(".")
print(sys.path)

import pandas as ps
from pandas_datareader import data as pdr
import yfinance as yfin
import matplotlib.pyplot as plt
from trading_indicator import TradingIndicator
yfin.pdr_override()

tesla_data = pdr.get_data_yahoo("AAPL", start="2020-01-01")

#%% Test MA, EWMA
ind = TradingIndicator(tesla_data)
MA_tesla = ind.ma(window_size=60)
EWMA_tesla = ind.ewma(span=30)
plt.plot(MA_tesla, label="MA")
plt.plot(EWMA_tesla, label="EWMA")
plt.plot(tesla_data["Adj Close"], label="Adj close")
plt.legend()

#%% Stochastic Oscillator
from trading_indicator import TradingIndicator
ind = TradingIndicator(tesla_data)
so = ind.stochastic_oscillator()

fig, ax1 = plt.subplots()

ax1.plot(so.index,so['%K'], label="%K", color="b")
#ax1.plot(so['%D'], label="%D")
ax2 = ax1.twinx() 
ax2.plot(so['Adj Close'], label="Adj Close")
ax1.axhline(20, linestyle='--', color="r")
ax1.axhline(80, linestyle="--", color="r")
fig.legend()

#%% MACD

from trading_indicator import TradingIndicator
ind = TradingIndicator(tesla_data)
macd = ind.macd()

plt.plot(macd["macd"], label='AMD MACD')
plt.plot(macd["signal"], label='Signal Line')
plt.legend(loc='upper left')
plt.show()

#%% Bollinger
from trading_indicator import TradingIndicator
ind = TradingIndicator(tesla_data)
boll_upper, boll_lower = ind.bollinger_bands()

plt.title(' Bollinger Bands')
plt.xlabel('Days')
plt.ylabel('Adj Close')
plt.plot(tesla_data["Adj Close"], label='Closing Prices')
plt.plot(boll_upper, label='Bollinger Up', c='g')
plt.plot(boll_lower, label='Bollinger Down', c='r')
plt.legend()

#%% 

from trading_indicator import TradingIndicator
ind = TradingIndicator(tesla_data)
rsi=ind.rsi()

fig, ax1 = plt.subplots()
ax1.plot(rsi, label="RSI Index", color="orange")
#ax1.plot(so['%D'], label="%D")
ax2 = ax1.twinx() 
ax2.plot(so['Adj Close'], label="Adj Close")
ax1.axhline(30, linestyle='--', color="r")
ax1.axhline(70, linestyle="--", color="r")
fig.legend()
