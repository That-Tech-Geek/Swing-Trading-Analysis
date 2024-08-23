import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import date

# Function to calculate RSI
def calculate_rsi(data, window):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Streamlit App
st.title("Swing Trading Stock Analyzer")

# User inputs
stock_symbol = st.text_input("Enter the stock symbol:", "AAPL")
start_date = st.date_input("Start Date", date(2023, 1, 1))
end_date = st.date_input("End Date", date.today())

# Fetch stock data
data = yf.download(stock_symbol, start=start_date, end=end_date)

# Calculate moving averages
data['20_MA'] = data['Close'].rolling(window=20).mean()
data['50_MA'] = data['Close'].rolling(window=50).mean()
data['200_MA'] = data['Close'].rolling(window=200).mean()

# Calculate RSI
data['RSI'] = calculate_rsi(data, 14)

# Plotting
st.subheader("Stock Price and Moving Averages")
plt.figure(figsize=(14, 7))
plt.plot(data['Close'], label='Close Price')
plt.plot(data['20_MA'], label='20-Day MA')
plt.plot(data['50_MA'], label='50-Day MA')
plt.plot(data['200_MA'], label='200-Day MA')
plt.legend(loc='best')
st.pyplot(plt)

st.subheader("RSI Indicator")
plt.figure(figsize=(14, 4))
plt.plot(data['RSI'], label='RSI')
plt.axhline(30, linestyle='--', alpha=0.5, color='red')
plt.axhline(70, linestyle='--', alpha=0.5, color='red')
plt.legend(loc='best')
st.pyplot(plt)

# Key Metrics for Swing Trading
st.subheader("Key Metrics for Swing Trading")

latest_close = data['Close'][-1]
latest_20_ma = data['20_MA'][-1]
latest_50_ma = data['50_MA'][-1]
latest_200_ma = data['200_MA'][-1]
latest_rsi = data['RSI'][-1]

st.write(f"**Latest Close Price:** {latest_close:.2f}")
st.write(f"**20-Day Moving Average:** {latest_20_ma:.2f}")
st.write(f"**50-Day Moving Average:** {latest_50_ma:.2f}")
st.write(f"**200-Day Moving Average:** {latest_200_ma:.2f}")
st.write(f"**RSI:** {latest_rsi:.2f}")

# Trading signal
st.subheader("Swing Trading Signal")
if latest_rsi < 30 and latest_close > latest_20_ma:
    st.success("The stock may be oversold and could present a buying opportunity.")
elif latest_rsi > 70 and latest_close < latest_20_ma:
    st.warning("The stock may be overbought and could be a selling opportunity.")
else:
    st.info("No strong signals for buying or selling at the moment.")
