import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go

def get_stock_data(symbol):
    # Download stock data from Yahoo Finance
    stock_data = yf.download(symbol, start="2020-01-01")
    return stock_data

def calculate_bollinger_bands(data, window=20):
    # Calculate moving average
    data['SMA'] = data['Close'].rolling(window).mean()
    # Calculate standard deviation
    data['STD'] = data['Close'].rolling(window).std()
    # Calculate Bollinger Bands
    data['Upper Band'] = data['SMA'] + (data['STD'] * 2)
    data['Lower Band'] = data['SMA'] - (data['STD'] * 2)
    return data

def plot_bollinger_bands(data, symbol):
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close Price'))
    fig.add_trace(go.Scatter(x=data.index, y=data['Upper Band'], mode='lines', name='Upper Band', line=dict(color='rgba(255, 0, 0, 0.5)')))
    fig.add_trace(go.Scatter(x=data.index, y=data['Lower Band'], mode='lines', name='Lower Band', line=dict(color='rgba(0, 0, 255, 0.5)')))
    fig.add_trace(go.Scatter(x=data.index, y=data['SMA'], mode='lines', name='SMA', line=dict(color='rgba(0, 255, 0, 0.5)')))

    fig.update_layout(title=f'Bollinger Bands for {symbol}', xaxis_title='Date', yaxis_title='Price')
    return fig

def main():
    st.title("Bollinger Bands Visualization")
    
    # Input for stock symbol
    symbol = st.text_input("Enter stock symbol", value="AAPL")
    
    if symbol:
        stock_data = get_stock_data(symbol)
        stock_data = calculate_bollinger_bands(stock_data)
        
        st.write(f"Displaying Bollinger Bands for {symbol}")
        fig = plot_bollinger_bands(stock_data, symbol)
        st.plotly_chart(fig)

if __name__ == "__main__":
    main()
