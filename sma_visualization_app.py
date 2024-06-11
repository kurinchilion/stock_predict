import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go

def get_stock_data(symbol):
    # Download stock data from Yahoo Finance
    stock_data = yf.download(symbol, start="2020-01-01")
    return stock_data

def calculate_sma(data, window=20):
    # Calculate the Simple Moving Average (SMA)
    data['SMA'] = data['Close'].rolling(window=window).mean()
    return data

def plot_sma(data, symbol, pass_color='red'):
    fig = go.Figure()

    # Plot the closing prices
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close Price'))
    
    # Plot the SMA
    fig.add_trace(go.Scatter(x=data.index, y=data['SMA'], mode='lines', name='SMA', line=dict(color=pass_color)))
    
    fig.update_layout(title=f'Simple Moving Average (SMA) for {symbol}', xaxis_title='Date', yaxis_title='Price')
    return fig

def main():
    st.title("Simple Moving Average (SMA) Visualization")
    
    # Input for stock symbol
    symbol = st.text_input("Enter stock symbol", value="AAPL")
    
    # Input for SMA window size
    window = st.number_input("Enter window size for SMA", min_value=1, value=20)
    
    if symbol:
        stock_data = get_stock_data(symbol)
        stock_data = calculate_sma(stock_data, window)
        
        st.write(f"Displaying Simple Moving Average (SMA) for {symbol} with a window size of {window} days")
        fig = plot_sma(stock_data, symbol)
        st.plotly_chart(fig)

        stock_data_200 = calculate_sma(stock_data, 200)
        fig2 = plot_sma(stock_data_200, symbol, 'blue')
        st.plotly_chart(fig2)

if __name__ == "__main__":
    main()
