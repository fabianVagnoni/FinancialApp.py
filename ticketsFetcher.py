# Fetches the tickers of S&P500 companies from Wikipedia

# Import necessary libraries (Wikipedia API and pandas)
import wikipedia
import pandas as pd

# Define the function that will gather and return the tickers
def retrieveTickets():

    # Gather the Wikipedia table containing the tickers in HTML format
    sp500_table = wikipedia.page("List of S&P 500 companies").html().encode("UTF-8")

    # Use pandas to read the HTML file and extract the symbol column as a list
    sp500_df = pd.read_html(sp500_table)[0]
    sp500_tickers = sp500_df['Symbol'].tolist()

    # Return the simbols column
    return sp500_tickers

