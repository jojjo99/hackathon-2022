#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 22:28:51 2022

@author: johanna
"""
# Strategy using rsi & macd
import sys
#sys.path.append(".")

import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yfin
import matplotlib.pyplot as plt

import numpy as np
yfin.pdr_override()

data = pdr.get_data_yahoo("WMT", start="2020-01-01")
"""
Contains the 10 top trading indicators in the material provided:
https://www.ig.com/en/trading-strategies/10-trading-indicators-every-trader-should-know-190604

These are implemented in a class to be used straight on time series.
"""

    

        
        
        
        
        
        
        
        
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
    enter_date = 0
    exit_date = 0
    returns = []
    for i in range(len(df)):
        if (df["buy"].iloc[i]==1 & long==False & (df["rsi"].iloc[i]<40)):
            long = True
            enter_price = df["Adj Close"].iloc[i]
            enter_date= df.index[i]
        elif(df["sell"].iloc[i]==1 & long==True & (df["rsi"].iloc[i]>60)):
            stop_price = df["Adj Close"].iloc[i]
            exit_date=df.index[i]
            returns.append([(stop_price-enter_price)/enter_price, enter_date, exit_date])
            long=False
            
    return returns
    

ret=backtest_macd(df)

buys = [ret[x][1] for x in range(len(ret))]
sell = [ret[x][2] for x in range(len(ret))]

#%%



buys_data = df.loc[buys]
sell_data = df.loc[buys]

plt.plot(df["Adj Close"], color="orange")
plt.scatter(buys, buys_data["Adj Close"] ,color="b")
plt.scatter(sell, sell_data["Adj Close"] ,color="r")


#mean=np.mean(ret[0])
#std = np.std(ret)



#%%


