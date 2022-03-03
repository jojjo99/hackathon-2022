#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 22:28:51 2022

@author: johanna
"""
# Strategy using rsi & macd
import sys
sys.path.append(".")

import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yfin
import matplotlib.pyplot as plt

import numpy as np
yfin.pdr_override()

data = pdr.get_data_yahoo("WMT", start="2015-01-01")
"""
Contains the 10 top trading indicators in the material provided:
https://www.ig.com/en/trading-strategies/10-trading-indicators-every-trader-should-know-190604

These are implemented in a class to be used straight on time series.
"""
import numpy as np

class TradingIndicator:
    
    # Obs time_series_data must be a df!
    def __init__(self, time_series_data):
        self.df = time_series_data

    # Simple MA with some default params
    def ma(self, window_size = 30, win_type='triang', col="Adj Close"):
        return self.df[col].rolling(window=window_size, win_type=win_type).mean()

    # Exponentially weighted MA
    def ewma(self, span = 10, adjust=False, col="Adj Close"):
        return self.df[col].ewm(span=span, adjust=adjust).mean()
    
     # Stochastic implementation.
    def stochastic_oscillator(self, span=14, ma_span=3, col="Adj Close"):
        data = self.df
        data["span_high"] = data.High.rolling(span).max()
        data["span_low"] = data.Low.rolling(span).min()
        data['%K'] = (data[col]- data['span_low'])*100/(data['span_high'] - data['span_low'])
        data['%D'] = data['%K'].rolling(ma_span).mean()
        return data
    
    # Moving average convergence divergence
    # Buy MACD over signal line.
    def macd(self, span1=12, span2=26, span_signal=9, col="Adj Close"):
        data = self.df
        
        data["macd"]=self.ewma(span=span1)-self.ewma(span=span2)
        data["signal"]=data["macd"].ewm(span=span_signal, adjust=False).mean()
        return data
    
    # Bollinger band for LT trading signals.
    # Trading signal sell when prices hit upper band, buy when prices hit lower band
    def bollinger_bands(self, rate=20, col="Adj Close"):
        sma = self.ma(window_size=rate)
        std = self.df[col].rolling(rate).std()
        bollinger_up = sma + std * 2 # Calculate top band
        bollinger_down = sma - std * 2 # Calculate bottom band
        return bollinger_up, bollinger_down
    
    # RSI indicator
    def rsi(self, periods=14, col="Adj Close", ema=True):
        deltas=self.df[col].diff(1)
     # Make two series: one for lower closes and one for higher closes
        up = deltas.clip(lower=0)
        down = -1 * deltas.clip(upper=0)
    
        if ema == True:
	    # Use exponential moving average
            ma_up = up.ewm(com = periods - 1, adjust=True, min_periods = periods).mean()
            ma_down = down.ewm(com = periods - 1, adjust=True, min_periods = periods).mean()
        else:
        # Use simple moving average
            ma_up = up.rolling(window = periods, adjust=False).mean()
            ma_down = down.rolling(window = periods, adjust=False).mean()
        
        rsi = ma_up / ma_down
        rsi = 100 - (100/(1 + rsi))
        return rsi
                
        
        
        
        
        
        
        
        
#%%
ind = TradingIndicator(data)
rsi=ind.rsi()
df = ind.macd()
df["rsi"]=rsi
signal = df["signal"]
macd= df["macd"]
df["diff"]=(signal-macd)
df["sign"] = np.sign(df["diff"])
df["buy"] = (df["sign"] > df["sign"].shift(1))*1
df["sell"] = (df["sign"] < df["sign"].shift(1))*1
buy_date=df[df["buy"]!=0].index
buy_price=df[df["buy"]!=0] ["Adj Close"]
sell_date=df[df["sell"]!=0].index
sell_price=df[df["sell"]!=0] ["Adj Close"]
plt.plot(data["Adj Close"], color="orange")
plt.scatter(buy_date, buy_price ,color="b")
plt.scatter(sell_date, sell_price ,color="r")

df["upper_bollinger"], df["lower_bollinger"]=ind.bollinger_bands()
df["boll_sell"]=df["upper_bollinger"]<df["Adj Close"]
df["boll_buy"]=df["lower_bollinger"]>df["Adj Close"]

df=df.dropna()

def backtest_macd(df):
    long=False
    enter_price = 0
    close_price = 0
    returns = []
    for i in range(len(df)):
        if (df["buy"].iloc[i]==1 & long==False & ((df["rsi"].iloc[i]<30))):
            long = True
            enter_price = df["Adj Close"].iloc[i]
        elif(df["sell"].iloc[i]==1 & long==True & (df["rsi"].iloc[i]>60)):
            long=False
            stop_price = df["Adj Close"].iloc[i]
            returns.append((stop_price-enter_price)/enter_price)
            
    return returns
    

ret=backtest_macd(df)
mean=np.mean(ret)
std = np.std(ret)





