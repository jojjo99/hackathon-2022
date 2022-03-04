#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 10:01:19 2022

@author: johanna
"""

import linchackathon as ls
import pandas as pd
data = pd.DataFrame(ls.getStockHistory('all', 100) )

#%%
data ['Close' ] = (data ['bidClose'] + data ['askClose'] ) / 2
df = data.pivot('time', 'symbol', 'Close')
#data [ ’ ] = ( data [ ’ bi dCl o s e ’ ] + data [ ’ a s kCl o s e ’ ] ) / 2