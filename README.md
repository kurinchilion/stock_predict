### Finance with Python Streamlit
<p>create a Streamlit app with Plotly to visualize Bollinger Bands for a given stock symbol using Yahoo Finance data.</p>

####  Environment setup
``` shell
$ pip install virtualenv
$ virtualenv venv
$ ./venv/Scripts/activate (for windows)
$ source venv/bin/activate (for mac)
```

###  Bollinger Band


Bollinger Bands are a type of technical analysis tool defined by a set of trendlines plotted two standard deviations (positively and negatively) away from a simple moving average (SMA) of a security's price. This method was developed by John Bollinger in the 1980s.

##### Components of Bollinger Bands:
<p><strong>Middle Band</strong>: This is the simple moving average (SMA) of the security's price, usually set to 20 periods.</p>
<p><strong>Upper Band</strong>: This is the SMA plus two standard deviations of the price.</p>
<p><strong>Lower Band</strong>: This is the SMA minus two standard deviations of the price.</p>

##### Interpretation:
<p><strong>Width of Bands</strong>: Indicates volatility. When the bands are wider, volatility is high; when they are narrower, volatility is low.</p>
<p><strong>Price Relationship</strong>: If the price moves towards the upper band, it may be overbought. If the price moves towards the lower band, it may be oversold.</p>


```shell
$ touch bollinger_bands.py
$ pip install streamlit plotly yfinance pandas
```

####  Bollinger Band Code Explanation

<p><strong>Data Retrieval</strong>: The get_stock_data function uses the yfinance library to download historical stock data from Yahoo Finance.</p>
<p>Bollinger Bands Calculation</strong>: The calculate_bollinger_bands function calculates the Simple Moving Average (SMA), the standard deviation, and the upper and lower Bollinger Bands.</p>
<p><strong>Plotting</strong>: The plot_bollinger_bands function uses Plotly to create an interactive plot of the closing prices along with the Bollinger Bands.</p>
<p><strong>Streamlit App</strong>: The main function sets up the Streamlit interface, takes user input for the stock symbol, fetches and processes the data, and displays the Bollinger Bands plot.</p>


#### Running the Bollinger Band app
```shell
$ streamlit run bollinger_bands.py
```

<p>This app provides a user-friendly way to visualize Bollinger Bands for any given stock symbol using real-time data from Yahoo Finance.</p>


###  Bollinger Band Prediction
```shell
$ touch bollinger_band_prediction.py
$ pip install streamlit plotly yfinance pandas scikit-learn
```

##### Factors for Better Predictions
<p>A holistic approach combining technical analysis, fundamental analysis, and market sentiment can enhance the accuracy of stock price predictions. Here’s a step-by-step outline:</p>

<p><strong>Data Collection</strong>: Gather historical price data, company financials, and relevant news.</p>
<p><strong>Feature Engineering</strong>: Create relevant features such as moving averages, RSI, P/E ratios, etc.</p>
<p><strong>Model Selection</strong>: Choose appropriate models (e.g., Linear Regression, ARIMA, or machine learning models).</p>
<p><strong>Training and Testing</strong>: Train the model on historical data and validate its performance on a test set.</p>
<p><strong>Prediction and Analysis</strong>: Use the model to predict future prices and analyze the results in the context of broader market conditions.</p>


#### Running the Bollinger Band Prediction app
<p>Bollinger Bands for visualization and a simple Linear Regression model for prediction in a Streamlit app.</p>

```shell
$ streamlit run bollinger_band_prediction.py
```


###  Stock Price Prediction
<p>Streamlit app with Plotly to visualize and predict stock prices for a given symbol using Yahoo Finance data. A simple machine learning model -  Linear Regression is used for prediction.</p>

```shell
$ touch stock_price_prediction.py
$ pip install streamlit plotly yfinance pandas scikit-learn
```

##### Code Explanation
<p><strong>Data Retrieval</strong>: The get_stock_data function uses the yfinance library to download historical stock data from Yahoo Finance.</p>
<p><strong>Prediction</strong>: The predict_stock_prices function fits a Linear Regression model to the stock's closing prices and predicts future prices for the next 30 business days.</p>
<p><strong>Plotting</strong>: The plot_predictions function uses Plotly to create an interactive plot of the actual closing prices, the model's predictions on the test set, and the future price predictions.</p>
<p><strong>Streamlit App</strong>: The main function sets up the Streamlit interface, takes user input for the stock symbol, fetches and processes the data, and displays the predictions plot.</p>

<p> This app provides a simple way to visualize and predict stock prices for any given stock symbol using historical data from Yahoo Finance.</p>

```shell
$ streamlit run stock_price_prediction.py
```




###  Exponential Moving Average
<p>Exponential Moving Average is used to predict the direction of the trend.</p>

```shell
$ touch ema_visualization_app.py
$ pip install streamlit plotly yfinance pandas scikit-learn
```


<p><strong>Data Retrieval</strong>: The get_stock_data function uses the yfinance library to download historical stock data from Yahoo Finance.</p>
<p><strong>EMA Calculation</strong>: The calculate_ema function calculates the Exponential Moving Average (EMA) over a specified window (default is 20 periods).</p>
<p><strong>Plotting</strong>: The plot_ema function uses Plotly to create an interactive plot of the closing prices and the EMA.</p>
<p><strong>Streamlit App</strong>: The main function sets up the Streamlit interface, takes user input for the stock symbol, fetches and processes the data, and displays the EMA plot.</p>

<p>This app provides a user-friendly way to visualize the Exponential Moving Average for any given stock symbol using real-time data from Yahoo Finance.</p>

```shell
$ streamlit run ema_visualization_app.py
```


### Price Probability Calculator
```
$ pip install yfinance numpy pandas scipy streamlit plotly
```

**Streamlit Interface:**

<p>Create a title and input fields for the stock symbol, period, and future price.
Add a button to trigger the probability calculation.</p>

**Fetch Historical Data:**

<p>Use yfinance to fetch historical closing prices for the specified period.</p>

**Calculate Daily Returns:**

<p>Compute daily percentage returns from the closing prices.</p>

**Calculate Probability:**

<p>Use the cumulative distribution function (CDF) of the normal distribution to calculate the probability that the stock's price will be at or below a given future price.</p>

**Plot Data:**

<p>Use plotly to create an interactive line chart of the closing prices and display it using Streamlit.</p>

```shell
$ streamlit run price_probability_calculator.py
```

<p>This Streamlit app fetches historical stock data, calculates the probability of the stock reaching a specified future price based on historical returns, and plots the historical closing prices. You can further customize the app by adding more features or refining the calculations.</p>


### Price Probability Range
```
$ pip install yfinance numpy pandas scipy streamlit plotly
```

```shell
$ streamlit run price_probability_range.py
```

<p>This Streamlit app fetches historical stock data, calculates the probability of the stock reaching a specified future price based on historical returns, and plots the historical closing prices along with the predicted future prices and their confidence interval. You can further customize the app by adding more features or refining the calculations.</p>


