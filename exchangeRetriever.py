# Gather basic qualitative information about an exchange composite given the composite's ticker
# This information is likely if not certain to never require an update


# Import the necessary libraries (Yahoo! Finance API and time)
import yfinance as yf
import time

# Define the function to retrieve the data
def exchangeRetriever(security):

    # Ask the API for the connection to the ticker and sleep
    exchange = yf.Ticker(security)
    time.sleep(0.7)

    # Save the information of the ticker in a variable and extract from it the desired attributes
    comp = exchange.info
    city = comp['timeZoneFullName']
    currency = comp['currency']
    exchange = comp['exchange']

    # Return the attributes
    return city, currency, exchange


