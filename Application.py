import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import  timedelta
from module import Stock
from module import *

st.title("Nifty 50 Stock Selector")

start = st.date_input("Start", value = pd.to_datetime("2019/12/01"))
end = st.date_input("End", value = pd.to_datetime("2024-01-01"))
equity = st.number_input("Equity")
start = start - timedelta(30)

if equity > 0:
  s = Stock(start, end)
  
  all_monthly_ret = s.monthlyPrices()
  
  eq_port, eq_nifty, list_port, list_nifty, dates, months, monthly_mean_port, monthly_mean_nifty = cal(all_monthly_ret, equity) 
  
  
  st.set_option('deprecation.showPyplotGlobalUse', False)
  plt.title('Strategy vs Benchmark')
  plt.plot(dates,list_port, label="Strategy")
  plt.plot(dates,list_nifty, label="Benchmark")
  plt.xticks(rotation=45)
  fig = plt.legend(loc="upper left")
  fig = plt.show()
  st.pyplot(fig)
  s,b = f"Sharpe: {sharpe(monthly_mean_port):.2f}% CAGR%: {CAGR(list_port[0],list_port[-1], months/12):.2f}% Vol%: {volatility(monthly_mean_port):.2f}%", f"Sharpe: {sharpe(monthly_mean_nifty):.2f}% CAGR%: {CAGR(list_nifty[0], list_nifty[-1], months/12):.2f}% Vol%: {volatility(monthly_mean_nifty):.2f}%"
  st.write("Index: Strategy ")
  st.write(s)
  st.write("Index: Benchmark ")
  st.write(b)
