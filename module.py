import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from pandas.tseries.offsets import MonthEnd
import numpy as np


class Stock:
    def __init__(self, start, end):
        self.tickers = pd.read_html("https://en.wikipedia.org/wiki/NIFTY_50")[2].Symbol
        self.prices, self.symbols = [], []
        for self.symbol in self.tickers:
            self.df = yf.download(f"{self.symbol}.NS", start=start, end =end)["Adj Close"]
            self.prices.append(self.df)
            self.symbols.append(self.symbol)
        self.all_prices = pd.concat(self.prices, axis=1)
        self.all_prices.columns = self.symbols
        self.all_daily_returns = self.all_prices.pct_change()
    
    def curPrice(self, curDate):
        return self.all_prices.loc[curDate]

    def nDayRet(self, N, curDate):
        return self.all_prices.loc[curDate:].pct_change().resample(f"{N}D").agg(lambda x : (x + 1).prod() - 1)
    
    def dailyRet(self, curDate):
        return self.all_daily_returns.loc[curDate] 
    
    def last30DaysPrice(self, curDate):
        curDate = datetime.strptime(curDate, "%Y-%m-%d").date()
        date30DaysAgo = curDate - timedelta(30)
        return self.all_prices.loc[date30DaysAgo:curDate]
    
    def monthlyPrices(self):
        return self.all_prices.pct_change().resample("M").agg(lambda x : (x + 1).prod() - 1)
    

def cal(all_monthly, equity):
    all_monthly_forward = all_monthly
    portfolio_equity, nifty_equity = equity, equity
    mean_monthly_return_portfolio, mean_monthly_return_nifty = [], []
    months = 0
    #making lists to append equity and dates every month for plotting
    portfolio_equity_list, nifty_equity_list, datelist = [], [], []
    for row in range(len(all_monthly_forward) - 1 ):
        #For Plotting
        nifty_equity_list.append(nifty_equity)
        portfolio_equity_list.append(portfolio_equity)

        #getting the positive stocks and then calculating their returns for the next month
        win = all_monthly_forward.iloc[row].where(all_monthly_forward.iloc[0] > 0).dropna()
        win_ret = all_monthly.loc[win.name + MonthEnd(1), win.index]
        portfolio_equity += portfolio_equity * win_ret.mean()
        
        #For nifty
        win2 = all_monthly_forward.iloc[row]
        win_ret2 = all_monthly.loc[win2.name + MonthEnd(1), win2.index]
        nifty_equity += nifty_equity * win_ret2.mean()
        
        
        datelist.append(win2.name)
        

        #To summarize performance of Nifty and Portfolio
        mean_monthly_return_nifty.append(win_ret2.mean())
        mean_monthly_return_portfolio.append(win_ret.mean())
        months += 1
    
    dates = []
    for ts in datelist:
        dates.append((ts.to_pydatetime()))


    return portfolio_equity, nifty_equity, portfolio_equity_list, nifty_equity_list, dates, months, mean_monthly_return_portfolio, mean_monthly_return_nifty



def CAGR(start, end, periods):
    return ((end/start)**(1/periods) - 1) * 100

def volatility(monthly_return):
    return (np.array(monthly_return).std() * np.sqrt(12)) * 100

def sharpe(monthly_return):
    sd_return = np.array(monthly_return).std()
    mean_return = np.array(monthly_return).mean()
    
    return mean_return / sd_return * np.sqrt(12) 