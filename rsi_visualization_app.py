import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go

def get_stock_data(symbol):
    # Download stock data from Yahoo Finance
    stock_data = yf.download(symbol, start="2020-01-01")
    return stock_data

def calculate_rsi(data, window=14):
    # Calculate the RSI
    delta = data['Close'].diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    data['RSI'] = rsi
    return data

def plot_rsi(data, symbol):
    fig = go.Figure()

    # Plot the closing prices
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close Price', line=dict(color='black')))
    
    # Plot the RSI
    fig.add_trace(go.Scatter(x=data.index, y=data['RSI'], mode='lines', name='RSI', line=dict(color='orange')))
    
    # Add overbought/oversold zones
    fig.add_shape(type="line", x0=data.index[0], y0=70, x1=data.index[-1], y1=70, line=dict(color="red", dash="dash"))
    fig.add_shape(type="line", x0=data.index[0], y0=30, x1=data.index[-1], y1=30, line=dict(color="green", dash="dash"))
    
    fig.update_layout(title=f'Relative Strength Index (RSI) for {symbol}', xaxis_title='Date', yaxis_title='Price/RSI')
    return fig

def main():
    st.title("Relative Strength Index (RSI) Visualization")
    
    # Input for stock symbol
    symbol = st.text_input("Enter stock symbol", value="AAPL")
    
    if symbol:
        stock_data = get_stock_data(symbol)
        stock_data = calculate_rsi(stock_data)
        
        st.write(f"Displaying RSI for {symbol}")
        fig = plot_rsi(stock_data, symbol)
        st.plotly_chart(fig)

        st.write("Data Table")
        st.dataframe(stock_data[['Close', 'RSI']])

if __name__ == "__main__":
    main()
