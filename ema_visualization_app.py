import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go

def get_stock_data(symbol):
    # Download stock data from Yahoo Finance
    stock_data = yf.download(symbol, start="2020-01-01")
    return stock_data

def calculate_ema(data, window=20):
    # Calculate the Exponential Moving Average (EMA)
    data['EMA'] = data['Close'].ewm(span=window, adjust=False).mean()
    return data

def plot_ema(data, symbol):
    fig = go.Figure()

    # Plot the closing prices
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close Price'))
    
    # Plot the EMA
    fig.add_trace(go.Scatter(x=data.index, y=data['EMA'], mode='lines', name='EMA', line=dict(color='orange')))
    
    fig.update_layout(title=f'Exponential Moving Average (EMA) for {symbol}', xaxis_title='Date', yaxis_title='Price')
    return fig

def main():
    st.title("Exponential Moving Average (EMA) Visualization")
    
    # Input for stock symbol
    symbol = st.text_input("Enter stock symbol", value="AAPL")
    
    if symbol:
        stock_data = get_stock_data(symbol)
        stock_data = calculate_ema(stock_data,100)
        
        st.write(f"Displaying Exponential Moving Average (EMA) for {symbol}")
        fig = plot_ema(stock_data, symbol)
        st.plotly_chart(fig)

if __name__ == "__main__":
    main()
