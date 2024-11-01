# Gathers info from Yahoo! Finance about company's ratios
# This info will probably have to be updated once every quarter

# Import necessary libraries
import yfinance as yf
import time
from datetime import date


# Define the function to gather information
def gather_info_ratios(security):

    # Establish a connection the Yahoo! Finance API
    stock = yf.Ticker(security)
    time.sleep(0.66)

    # Calculate the quarter of today, so the file can run in any day and add the corresponding quarter of the information
    quarter = f"{date.today().year}-Q{((date.today().month - 1) // 3) + 1}"

    # Extract the desired ratios
    overall_risk = stock.info['overallRisk'] if 'overallRisk' in stock.info else None
    dividend_yield = stock.info['fiveYearAvgDividendYield'] if 'fiveYearAvgDividendYield' in stock.info else None
    beta = stock.info['beta'] if 'beta' in stock.info else None
    PE_ratio = stock.info['forwardPE'] if 'forwardPE' in stock.info else None
    gross_margin = stock.info['grossMargins'] if 'grossMargins' in stock.info else None
    quick_ratio = stock.info['quickRatio'] if 'quickRatio' in stock.info else None
    price_to_book_ratio = stock.info['priceToBook'] if 'priceToBook' in stock.info else None

    # Return all the attributes
    return quarter, overall_risk, dividend_yield, beta, PE_ratio, gross_margin, quick_ratio, price_to_book_ratio
