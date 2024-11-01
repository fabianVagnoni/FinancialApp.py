# Gather basic qualitative information about an index
# This information is likely to never require an update


# Import necessary libraries
import yfinance as yf
import time


# Define the function to gather and return the information
def indexRetriever(security):

    # Establish API connection and sleep
    exchange = yf.Ticker(security)
    time.sleep(0.7)

    # Retrieve desired information
    comp = exchange.info
    currency = comp['currency']
    typeQuote = comp['quoteType']
    shortName = comp['shortName']

    # Return the attributes
    return currency, typeQuote, shortName