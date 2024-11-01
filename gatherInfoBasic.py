# Gets the basic qualitative information about the stock
# That is, information that is likely to never have to be updated


# Import the necessary libraries
import yfinance as yf
import time


# Define the function to gather and return the information
def gather_info_basic(security):

    # Establish the connection to the API and sleep
    stock = yf.Ticker(security)
    time.sleep(0.66)

    # Save the desired information in variables, if this information is available
    company_name = stock.info['shortName'] if 'shortName' in stock.info else None
    sector = stock.info['sector'] if 'sector' in stock.info else None
    exchange = stock.info.get('exchange', 'Exchange not found')

    # Return the information
    return company_name, sector, exchange
