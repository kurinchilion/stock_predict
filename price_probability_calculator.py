import yfinance as yf
import numpy as np
import pandas as pd
from scipy.stats import norm
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime

def fetch_historical_data(symbol, period="1y"):
    stock = yf.Ticker(symbol)
    data = stock.history(period=period)
    return data['Close']

def calculate_daily_returns(data):
    returns = data.pct_change().dropna()
    return returns

def calculate_probability(current_price, future_price, mean, std_dev):
    z = (future_price - current_price - mean) / std_dev
    probability = norm.cdf(z)
    return probability

def plot_data(data, symbol):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data, mode='lines', name='Close Price'))
    fig.update_layout(title=f"Closing Prices for {symbol}",
                      xaxis_title="Date",
                      yaxis_title="Price")
    st.plotly_chart(fig)

st.title("Yahoo Finance Price Probability Calculator")

symbol = st.text_input("Enter the stock symbol", value='AAPL')
period = st.selectbox("Select the historical data period", options=['1y', '6mo', '1mo'])
future_price = st.number_input("Enter the future price to calculate the probability for", value=150.0)

if st.button("Calculate Probability"):
    # Fetch historical data
    data = fetch_historical_data(symbol, period)
    current_price = data[-1]

    # Calculate daily returns
    returns = calculate_daily_returns(data)

    # Calculate mean and standard deviation of returns
    mean = returns.mean()
    std_dev = returns.std()

    # Calculate probability
    probability = calculate_probability(current_price, future_price, mean, std_dev)

    st.write(f"Current price of {symbol}: {current_price}")
    st.write(f"Mean daily return: {mean}")
    st.write(f"Standard deviation of daily returns: {std_dev}")
    st.write(f"Probability that the price will be at or below {future_price}: {probability:.2%}")

    # Plot the data
    plot_data(data, symbol)
