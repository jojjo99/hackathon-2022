#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 11:53:34 2022

@author: johanna
"""
import linchackathon as lh
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
def prepare_input_data(df, security):
    df['Close' ] = (df ['bidClose'] + df ['askClose'] ) / 2
    df['High']=(data['bidHigh']+ data['askHigh'])/2
    df['Low']=(data['bidLow']+ data['bidLow'])/2
    
    high_close = np.abs(df['High']-df['Close'].shift())
    low_close = np.abs(df['Low']-df['Close'].shift())
    high_low = df['High']-df['Low']
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = np.max(ranges, axis=1)
    atr = true_range.rolling(14).sum()/14
    df["ATR"]=atr
    
    df["Max_high"] = df["High"].rolling(22, min_periods=22).max()  
    df["Ch_exit_long"] = df["Max_high"] - df["ATR"] * 3
    return df

    
#%%
    stock_new=stock_new.dropna()
    ind = TradingIndicator(stock_new)

    rsi=ind.rsi(9, security)
    df2 = ind.macd(12, 26, 9, security)
    df2["rsi"]=rsi
    signal = df2["signal"]
    macd= df2["macd"]
    
    df2["diff"]=(signal-macd)
    df2["sign"] = np.sign(df2["diff"])
    df2["buy"] = (df2["sign"] > df2["sign"].shift(1))*1
    df2["sell"] = (df2["sign"] < df2["sign"].shift(1))*1
    return df2


#%%
data = pd.DataFrame(ls.getStockHistory('all', 100) )
#%%
ticker="BOND1"
df = data[data["symbol"]==ticker]
#%%

df2=prepare_input_data(df, ticker)
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



def prepare_input_data(df, security):
    stock = df[security].to_frame()
    stock.index=pd.to_datetime(stock.index)
    stock_new=stock.resample('1H').last() #
    stock_new=stock_new.dropna()
    ind = TradingIndicator(stock_new)

    rsi=ind.rsi(9, security)
    df2 = ind.macd(12, 26, 9, security)
    df2["rsi"]=rsi
    signal = df2["signal"]
    macd= df2["macd"]
    
    df2["diff"]=(signal-macd)
    df2["sign"] = np.sign(df2["diff"])
    df2["buy"] = (df2["sign"] > df2["sign"].shift(1))*1
    df2["sell"] = (df2["sign"] < df2["sign"].shift(1))*1
    return df2
    


def backtest_macd(df, stock):
    long=False
    enter_price = 0
    close_price = 0
    enter_date = 0
    exit_date = 0
    returns = []
    for i in range(len(df)):
        if (df["buy"].iloc[i]==1 & long==False & (df["rsi"].iloc[i]<70)):
            long = True
            enter_price = df[stock].iloc[i]
            enter_date= df.index[i]
        elif(df["sell"].iloc[i]==1 & long==True & (df["rsi"].iloc[i]>30)):
            stop_price = df[stock].iloc[i]
            exit_date=df.index[i]
            returns.append([(stop_price-enter_price)/enter_price, enter_date, exit_date])
            long=False
            
    return returns


def trade(df, stock, weights):
    #current_portfolio = lh.getPortfolio()
   # print(current_portfolio)
    long=True
    #if stock in current_portfolio:
        #long=True
    #else:
        #long = False
    enter_price = 0
    close_price = 0
    enter_date = 0
    exit_date = 0
    returns = []
    if (df["buy"].iloc[-1]==1 & long==False & (df["rsi"].iloc[-1]<70)):
        long = True
        weight = weights[stock]
        amount = lh.getSaldo()*weight
        nbr_share = (amount/df[stock].iloc[-1]).round()
        print(stock, nbr_share)
        #lh.buyStock(stock, nbr_share)
        enter_price = df[stock].iloc[-1]
        enter_date= df.index[-1]
        
    elif(df["sell"].iloc[-1]==1 & long==True & (df["rsi"].iloc[-1]>30)):
        print(stock, nbr_share)
        #lh.sellStock(stock, nbr_share)
        stop_price = df[stock].iloc[-1]
        exit_date=df.index[-1]
        returns.append([(stop_price-enter_price)/enter_price, enter_date, exit_date])
        long=False
            
    return returns


def main_trading(data_all, securities):
    bond_weights = 0.4
    stock_weights = 0.6
    init_cash = 100000
    bond_cash = bond_weights*init_cash
    stock_cash = stock_weights*init_cash
    weightA = 0.175 # Top performing, Stock 7, 1, 3, 4
    weightB = 0.05 # avg performing # Stock 2, 10, 6, 5
    weightC = 0.01 # 9, 8
    
    weightD = 0.3 # Bond2
    weightE = 0.1 # Bond1
    weights = {"STOCK1":weightA, "STOCK7":weightA, "STOCK3":weightA, "STOCK4": weightA, 
                   "STOCK2": weightB, "STOCK10": weightB, "STOCK6": weightB, "STOCK5": weightB, 
                   "STOCK9":weightC, "STOCK8":weightC, "BOND1":weightE, "BOND2":weightD}

    # Trade bonds
    ret_total = []
    data_all ['Close' ] = (data_all ['bidClose'] + data_all ['askClose'] ) / 2
    df = data_all.pivot('time', 'symbol', 'Close')
    for i in range(0,2):
        security = securities[0]
        security_data = prepare_input_data(df, security)
        trade(security_data, security, weights)

    # Trade stocks

#%%
    for i in range(3,9):
            security = securities[i]
            security_data = prepare_input_data(data_all, security)
            trade(security_data, security, weights)
            #mean=np.mean(ret[0])
            #print(mean)
        
    return ret_total
    
    
    
#%%   
securities = lh.getTickers()
#%%
def main (securities):
    while True:
        data = pd.DataFrame(lh.getStockHistory('all', 30))
        main_trading(data, securities)
#%%
main_trading(data.iloc[:10000], securities)
    
 #%%

security="STOCK2"
df3=prepare_input_data(data, security)
ret=backtest_macd(df3, security)




#%%
buys = [ret[x][1] for x in range(len(ret))]
sell = [ret[x][2] for x in range(len(ret))]




buys_data = df3.loc[buys]
sell_data = df3.loc[buys]

#plt.plot(df3[security], color="orange")
#plt.scatter(buys, buys_data[security] ,color="b")
#plt.scatter(sell, sell_data[security] ,color="r")