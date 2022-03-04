#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 09:51:40 2022

@author: emildamirov
"""

import linchackathon as lh
import pandas as pd
import seaborn as sns
from datetime import datetime

lh.getStockHistory('all', 30)
data = pd.DataFrame(lh.getStockHistory('all', 30))

data['Close'] = (data['bidClose'] + data['askClose'])/2
stocks = data.pivot('time','symbol','Close')

#%%

stocks_returns = stocks.pct_change()

stocks_mean_returns = stocks_returns.mean()
stocks_mean_returns= stocks_mean_returns.sort_values(ascending=False)

stocks_std_returns = stocks_returns.std()
stocks_std_returns = stocks_std_returns.sort_values(ascending=False)

stocks_sharpe = stocks_mean_returns/stocks_std_returns
stocks_sharpe = stocks_sharpe.sort_values(ascending=False)


#%%

df1 = stocks['BOND2'].dropna()
df1 = df1.to_datetime

