# Gathers information about the values of a security


# Import necessary libraries
import yfinance as yf
import time
import numpy as np


# Function to gather and return information
# The parameter daily controls how much time of information will be retrieved
# If daily is set to true, the function will be retrieve just 24h of information (the daily update of the DB)
# If it is unchanged or manually set to False, it will retrieve all possible data
def gatherInfoValue(security , daily=False):
    # Connect to Yahoo! Finance API
    stock = yf.Ticker(security)
    time.sleep(0.66)

    # Extract all the required historical information
    # 24h of information if daily is true, else, all possible information
    if daily:
        historical_data = stock.history(period='1d')
    else:
        historical_data = stock.history(period='max')

    # If there is not information available, return all None
    if historical_data.empty:
        print('No historical')
        tradingDates, volatility, volume, close = None, None, None, None

    # If there is information available, return the dates for which there is information available in the shape
    # ignoring the hours; the closing price; the volume of trading; and the volatility calculated as the
    # standard deviation of the closing price over the period
    else:
        tradingDates = historical_data['Close'].index.strftime('%Y-%m-%d')
        close = historical_data['Close'].tolist()
        volatility = round(np.std(close), 3)
        volume = historical_data['Volume'].tolist()

    # Return all attributes
    return tradingDates, volatility, volume, close
