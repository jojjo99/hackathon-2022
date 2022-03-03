#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 21:46:34 2022

@author: johanna
"""

class PortfolioManagement:
    
    def __init__(self, initial_portfolio, logs):
        self.portfolio = initial_portfolio
        self.logs = logs
        
    def update_portfolio(self, new_portfolio):
        self.portfolio = new_portfolio
        self.logs = logs

        
    def get_portfolio_volatility(self):
        pass
    
        