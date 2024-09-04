import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.stats import norm
import datetime

# Function to fetch stock data
def fetch_stock_data(symbol):
    stock = yf.Ticker(symbol)
    data = stock.history(period='1y')
    return data

# Black-Scholes model for option pricing
def black_scholes(S, K, T, r, sigma, option_type='call'):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if option_type == 'call':
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == 'put':
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    return price

# Greeks calculation
def calculate_greeks(S, K, T, r, sigma, option_type='call'):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    delta = norm.cdf(d1) if option_type == 'call' else -norm.cdf(-d1)
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    theta = - (S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * (norm.cdf(d2) if option_type == 'call' else norm.cdf(-d2))
    vega = S * norm.pdf(d1) * np.sqrt(T)
    rho = K * T * np.exp(-r * T) * (norm.cdf(d2) if option_type == 'call' else -norm.cdf(-d2))
    return delta, gamma, theta, vega, rho

# Calculate P/L, break-even points, and loss percentage
def calculate_pl_and_break_even(option_legs, S, r, T, sigma):
    aggregate_pl = np.zeros_like(S)
    for leg in option_legs:
        K, option_type, quantity, option_price = leg
        pl = np.zeros_like(S)
        for i, s in enumerate(S):
            bs_price = black_scholes(s, K, T, r, sigma, option_type)
            pl[i] = quantity * (bs_price - option_price)
        aggregate_pl += pl
    break_even_points = S[np.isclose(aggregate_pl, 0, atol=0.01)]
    loss_percentage = np.sum(aggregate_pl < 0) / len(aggregate_pl) * 100
    return aggregate_pl, break_even_points, loss_percentage

# Main function to run the Streamlit app
def main():
    st.title("Option Strategy Simulator")

    # User inputs
    symbol = st.text_input("Enter the stock symbol:", value='AAPL')
    r = st.number_input("Enter the risk-free rate (annual, in decimal):", value=0.01)
    T_days = st.number_input("Enter the time to maturity (in days):", value=30)
    sigma = st.number_input("Enter the volatility (annual, in decimal):", value=0.2)
    
    T = T_days / 365
    
    num_legs = st.number_input("Enter the number of option legs (1 or 2):", value=1, min_value=1, max_value=2)
    
    option_legs = []
    for i in range(num_legs):
        st.subheader(f"Leg {i+1}")
        K = st.number_input(f"Enter the strike price for leg {i+1}:", value=150.0)
        option_type = st.selectbox(f"Select the option type for leg {i+1}:", options=['call', 'put'])
        quantity = st.number_input(f"Enter the quantity for leg {i+1}:", value=1)
        option_price = st.number_input(f"Enter the option price for leg {i+1}:", value=10.0)
        option_legs.append((K, option_type, quantity, option_price))
    
    # Fetch stock data
    data = fetch_stock_data(symbol)
    S = data['Close'].values
    
    # Calculate P/L, break-even points, and loss percentage
    pl, break_even_points, loss_percentage = calculate_pl_and_break_even(option_legs, S, r, T, sigma)
    
    # Calculate Greeks
    aggregate_greeks = np.zeros(5)
    for leg in option_legs:
        K, option_type, quantity, option_price = leg
        delta, gamma, theta, vega, rho = calculate_greeks(S[-1], K, T, r, sigma, option_type)
        aggregate_greeks += np.array([delta, gamma, theta, vega, rho]) * quantity

    # Display results
    st.write(f"Aggregate Greeks: Delta: {aggregate_greeks[0]}, Gamma: {aggregate_greeks[1]}, Theta: {aggregate_greeks[2]}, Vega: {aggregate_greeks[3]}, Rho: {aggregate_greeks[4]}")
    st.write(f"Break-even points: {break_even_points}")
    st.write(f"Loss percentage: {loss_percentage:.2f}%")
    
    # Plot P/L graph
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=S, y=pl, mode='lines', name='P/L'))
    fig.update_layout(title="P/L vs Stock Price",
                      xaxis_title="Stock Price",
                      yaxis_title="P/L")
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()
