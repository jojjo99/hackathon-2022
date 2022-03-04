#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 11:53:34 2022

@author: johanna
"""
import linchackathon as ls
import pandas as pd
import matplotlib.pyplot as plt
#%%
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
data = pd.DataFrame(ls.getStockHistory('all', 100) )
#%%
import numpy as np
data ['Close' ] = (data ['bidClose'] + data ['askClose'] ) / 2
df = data.pivot('time', 'symbol', 'Close')
stock = df["STOCK1"].to_frame()
stock.index=pd.to_datetime(stock.index)
stock_new=stock.resample('1H').last() #
stock_new=stock_new.dropna()
ind = TradingIndicator(stock_new)

rsi=ind.rsi(9, "STOCK1")
df2 = ind.macd(12, 26, 9, "STOCK1")
df2["rsi"]=rsi
signal = df2["signal"]
macd= df2["macd"]
#%%
df2["diff"]=(signal-macd)
df2["sign"] = np.sign(df2["diff"])
df2["buy"] = (df2["sign"] > df2["sign"].shift(1))*1
df2["sell"] = (df2["sign"] < df2["sign"].shift(1))*1
#plt.plot(stock_new)
#%%¨

def prepare_input_data(data_all, security):
    data_all ['Close' ] = (data_all ['bidClose'] + data_all ['askClose'] ) / 2
    df = data.pivot('time', 'symbol', 'Close')
    stock = df["STOCK1"].to_frame()
    stock.index=pd.to_datetime(stock.index)
    stock_new=stock.resample('1H').last() #
    stock_new=stock_new.dropna()
    ind = TradingIndicator(stock_new)

    rsi=ind.rsi(9, "STOCK1")
    df2 = ind.macd(12, 26, 9, "STOCK1")
    df2["rsi"]=rsi
    signal = df2["signal"]
    macd= df2["macd"]
    


def backtest_macd(df, stock):
    long=False
    enter_price = 0
    close_price = 0
    enter_date = 0
    exit_date = 0
    returns = []
    for i in range(len(df)):
        if (df["buy"].iloc[i]==1 & long==False & (df["rsi"].iloc[i]<40)):
            long = True
            enter_price = df[stock].iloc[i]
            enter_date= df.index[i]
        elif(df["sell"].iloc[i]==1 & long==True & (df["rsi"].iloc[i]>60)):
            stop_price = df[stock].iloc[i]
            exit_date=df.index[i]
            returns.append([(stop_price-enter_price)/enter_price, enter_date, exit_date])
            long=False
            
    return returns



ret=backtest_macd(df2, "STOCK1")
