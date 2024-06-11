import streamlit as st
import yfinance as yf
import pandas as pd

def get_option_chain(symbol):
    stock = yf.Ticker(symbol)
    opt_chain = stock.option_chain()
    puts = opt_chain.puts
    return puts

def calculate_credit_spread(puts, sell_strike, buy_strike):
    sell_price = puts.loc[puts['strike'] == sell_strike, 'lastPrice'].values[0]
    buy_price = puts.loc[puts['strike'] == buy_strike, 'lastPrice'].values[0]
    credit_spread = sell_price - buy_price
    return sell_price, buy_price, credit_spread

def main():
    st.title("Bull Put Credit Spread")
    
    # Input for stock symbol
    symbol = st.text_input("Enter stock symbol", value="AAPL")
    
    if symbol:
        try:
            puts = get_option_chain(symbol)
            st.write(f"Displaying put options for {symbol}")
            st.dataframe(puts)
            
            # Input for sell and buy strike prices
            sell_strike = st.selectbox("Select strike price to sell (put option)", puts['strike'])
            buy_strike = st.selectbox("Select strike price to buy (put option)", puts['strike'])
            
            if sell_strike and buy_strike:
                sell_price, buy_price, credit_spread = calculate_credit_spread(puts, sell_strike, buy_strike)
                
                st.write(f"Put Sell Strike Price: {sell_strike} - Last Price: ${sell_price:.2f}")
                st.write(f"Put Buy Strike Price: {buy_strike} - Last Price: ${buy_price:.2f}")
                st.write(f"Credit Spread: ${credit_spread:.2f}")
        except Exception as e:
            st.write("An error occurred while retrieving the option chain data. Please try again.")
            st.write(str(e))

if __name__ == "__main__":
    main()
