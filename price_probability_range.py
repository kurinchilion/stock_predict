import yfinance as yf
import numpy as np
import pandas as pd
from scipy.stats import norm
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta

def fetch_historical_data(symbol, period="1y"):
    stock = yf.Ticker(symbol)
    data = stock.history(period=period)
    return data['Close']

def calculate_daily_returns(data):
    returns = data.pct_change().dropna()
    return returns

def predict_future_price(current_price, mean, std_dev, days):
    future_price = current_price * np.exp((mean - 0.5 * std_dev**2) * days + std_dev * np.sqrt(days) * np.random.normal())
    return future_price

def plot_data(data, symbol, predicted_prices, days):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data, mode='lines', name='Close Price'))
    
    future_dates = [data.index[-1] + timedelta(days=i) for i in range(1, days + 1)]
    fig.add_trace(go.Scatter(x=future_dates, y=predicted_prices, mode='lines', name='Predicted Price'))

    fig.update_layout(title=f"Closing Prices and Predicted Prices for {symbol}",
                      xaxis_title="Date",
                      yaxis_title="Price")
    st.plotly_chart(fig)

st.title("Yahoo Finance Price Probability Calculator")

symbol = st.text_input("Enter the stock symbol", value='AAPL')
period = st.selectbox("Select the historical data period", options=['1y', '6mo', '1mo'])
days = st.number_input("Enter the number of days to predict into the future", value=30, min_value=1)
confidence_level = st.slider("Select the confidence level", min_value=0.0, max_value=1.0, value=0.95)

if st.button("Calculate Probability"):
    # Fetch historical data
    data = fetch_historical_data(symbol, period)
    current_price = data[-1]

    # Calculate daily returns
    returns = calculate_daily_returns(data)

    # Calculate mean and standard deviation of returns
    mean = returns.mean()
    std_dev = returns.std()

    # Predict future prices
    predicted_prices = [predict_future_price(current_price, mean, std_dev, i) for i in range(1, days + 1)]

    # Calculate confidence interval
    ci_lower = np.percentile(predicted_prices, (1 - confidence_level) / 2 * 100)
    ci_upper = np.percentile(predicted_prices, (1 + confidence_level) / 2 * 100)

    st.write(f"Current price of {symbol}: {current_price}")
    st.write(f"Mean daily return: {mean}")
    st.write(f"Standard deviation of daily returns: {std_dev}")
    st.write(f"Predicted price range for the next {days} days with {confidence_level * 100:.2f}% confidence: {ci_lower} - {ci_upper}")

    # Plot the data
    plot_data(data, symbol, predicted_prices, days)
