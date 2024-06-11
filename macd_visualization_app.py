import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go

def get_stock_data(symbol):
    # Download stock data from Yahoo Finance
    stock_data = yf.download(symbol, start="2020-01-01")
    return stock_data

def calculate_macd(data, short_window=12, long_window=26, signal_window=9):
    # Calculate the Short-term EMA
    data['ShortEMA'] = data['Close'].ewm(span=short_window, adjust=False).mean()
    # Calculate the Long-term EMA
    data['LongEMA'] = data['Close'].ewm(span=long_window, adjust=False).mean()
    # Calculate the MACD Line
    data['MACD'] = data['ShortEMA'] - data['LongEMA']
    # Calculate the Signal Line
    data['Signal Line'] = data['MACD'].ewm(span=signal_window, adjust=False).mean()
    return data

def plot_macd(data, symbol):
    fig = go.Figure()

    # Plot the closing prices
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close Price', line=dict(color='black')))
    
    # Plot the MACD Line
    fig.add_trace(go.Scatter(x=data.index, y=data['MACD'], mode='lines', name='MACD', line=dict(color='blue')))
    
    # Plot the Signal Line
    fig.add_trace(go.Scatter(x=data.index, y=data['Signal Line'], mode='lines', name='Signal Line', line=dict(color='red')))
    
    fig.update_layout(title=f'Moving Average Convergence Divergence (MACD) for {symbol}', xaxis_title='Date', yaxis_title='Price')
    return fig

def main():
    st.title("Moving Average Convergence Divergence (MACD) Visualization")
    
    # Input for stock symbol
    symbol = st.text_input("Enter stock symbol", value="AAPL")
    
    if symbol:
        stock_data = get_stock_data(symbol)
        stock_data = calculate_macd(stock_data)
        
        st.write(f"Displaying MACD for {symbol}")
        fig = plot_macd(stock_data, symbol)
        st.plotly_chart(fig)

        st.write("Data Table")
        st.dataframe(stock_data[['Close', 'MACD', 'Signal Line']])

if __name__ == "__main__":
    main()
