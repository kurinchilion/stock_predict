import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np

def get_stock_data(symbol):
    # Download stock data from Yahoo Finance
    stock_data = yf.download(symbol, start="2020-01-01")
    return stock_data

def predict_stock_prices(data):
    data['Date'] = data.index
    data['Date'] = pd.to_datetime(data['Date']).map(pd.Timestamp.timestamp)
    X = data['Date'].values.reshape(-1, 1)
    y = data['Close'].values
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    future_dates = pd.date_range(start=data.index[-1], periods=30, freq='B').to_pydatetime()
    future_timestamps = np.array([pd.Timestamp(date).timestamp() for date in future_dates]).reshape(-1, 1)
    future_predictions = model.predict(future_timestamps)
    
    return y_test, y_pred, future_dates, future_predictions

def plot_predictions(data, y_test, y_pred, future_dates, future_predictions, symbol):
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close Price'))
    fig.add_trace(go.Scatter(x=data.index[-len(y_test):], y=y_test, mode='lines', name='Actual Prices', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=data.index[-len(y_test):], y=y_pred, mode='lines', name='Predicted Prices', line=dict(color='red')))
    fig.add_trace(go.Scatter(x=future_dates, y=future_predictions, mode='lines', name='Future Predictions', line=dict(color='green')))

    fig.update_layout(title=f'Stock Price Prediction for {symbol}', xaxis_title='Date', yaxis_title='Price')
    return fig

def main():
    st.title("Stock Price Prediction")
    
    # Input for stock symbol
    symbol = st.text_input("Enter stock symbol", value="AAPL")
    
    if symbol:
        stock_data = get_stock_data(symbol)
        y_test, y_pred, future_dates, future_predictions = predict_stock_prices(stock_data)
        
        st.write(f"Displaying stock price predictions for {symbol}")
        fig = plot_predictions(stock_data, y_test, y_pred, future_dates, future_predictions, symbol)
        st.plotly_chart(fig)

if __name__ == "__main__":
    main()
