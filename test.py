#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 10:01:19 2022

@author: johanna
"""

import linchackathon as ls
import pandas as pd
import matplotlib.pyplot as plt
data = pd.DataFrame(ls.getStockHistory('all', 30) )

#%%
data ['Close' ] = (data ['bidClose'] + data ['askClose'] ) / 2
df = data.pivot('time', 'symbol', 'Close')
#data [ ’ ] = ( data [ ’ bi dCl o s e ’ ] + data [ ’ a s kCl o s e ’ ] ) / 2
#plt.plot(df["STOCK1"])
#df = df.groupby([df.index.dt.date]).mean()
#%% Chech Stock 
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
        
        data["macd"]=self.ewma(span=span1, col=col)-self.ewma(span=span2, col=col)
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
%%
# Chandelier exit snippet


 # high_low = df['High'] - df['Low']
 #   high_close = np.abs(df['High'] - df['Close'].shift())
 #   low_close = np.abs(df['Low'] - df['Close'].shift())
 #   ranges = pd.concat([high_low, high_close, low_close], axis=1)
 #   true_range = np.max(ranges, axis=1)
 #   ATR = true_range.rolling(22).sum()/14
 #   df['ATR'] = ATR

    # Chandelier exit

    ## for long position
 #   df["Max_high"] = df.rolling(22, min_periods=22)['High'].max()  
 #   df["Ch_exit_long"] = df["Max_high"] - df["ATR"] * 3
    
    ## for short position
  #  df["Lowest_low"] = df.rolling(22, min_periods=22)['Low'].min()  
  #  df["Ch_exit_short"] = df["Lowest_low"] + df["ATR"] * 3

#%%

import sys
from datetime import datetime 
#from trading_indicator import TradingIndicator

stock = df["STOCK1"].to_frame()
ind = TradingIndicator(stock)
rsi=ind.rsi(9, "STOCK1")
df2 = ind.macd(12, 26, 9, "STOCK1")
df2["rsi"]=rsi
stock.index=pd.to_datetime(stock.index)
test=stock.resample('1H').mean()
