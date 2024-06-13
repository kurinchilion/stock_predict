import yfinance as yf
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

def fetch_historical_data(symbol, period="1y"):
    stock = yf.Ticker(symbol)
    data = stock.history(period=period)
    return data['Close']

def calculate_rsi(data, window=14, method='wilder'):
    delta = data.diff().dropna()
    gain = (delta.where(delta > 0, 0)).fillna(0)
    loss = (-delta.where(delta < 0, 0)).fillna(0)
    
    if method == 'wilder':
        avg_gain = gain.ewm(alpha=1/window, min_periods=window).mean()
        avg_loss = loss.ewm(alpha=1/window, min_periods=window).mean()
    elif method == 'sma':
        avg_gain = gain.rolling(window=window, min_periods=window).mean()
        avg_loss = loss.rolling(window=window, min_periods=window).mean()
    elif method == 'ema':
        avg_gain = gain.ewm(span=window, adjust=False).mean()
        avg_loss = loss.ewm(span=window, adjust=False).mean()
    else:
        raise ValueError("Method must be one of 'wilder', 'sma', or 'ema'")
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def plot_data(data, rsi, symbol, method):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data, mode='lines', name='Close Price'))
    fig.add_trace(go.Scatter(x=rsi.index, y=rsi, mode='lines', name=f'RSI ({method})'))
    fig.update_layout(title=f"{symbol} Closing Prices and RSI ({method})",
                      xaxis_title="Date",
                      yaxis_title="Price/RSI")
    st.plotly_chart(fig)

st.title("Yahoo Finance RSI Calculator")

symbol = st.text_input("Enter the stock symbol", value='AAPL')
period = st.selectbox("Select the historical data period", options=['1y', '6mo', '3mo', '1mo'])
window = st.number_input("Enter the RSI calculation window", value=14, min_value=1)
method = st.selectbox("Select the RSI calculation method", options=['wilder', 'sma', 'ema'])

if st.button("Calculate RSI"):
    # Fetch historical data
    data = fetch_historical_data(symbol, period)

    # Calculate RSI
    rsi = calculate_rsi(data, window=window, method=method)

    st.write(f"RSI ({method}) for {symbol} with window {window}")
    st.write(rsi.tail())

    # Plot the data
    plot_data(data, rsi, symbol, method)
