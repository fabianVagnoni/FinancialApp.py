# Creates a JSON file with the basic structure of the DB following the ER Model
# & filling the Stock, Index and Exchanges entities with static qualitative data


# Import necessary libraries and other files
import json
import ticketsFetcher
import gatherInfoBasic
import exchangeRetriever
import indexRetriever


# Define the main function of this file
def jsonFileCreator():
    # Create an empty dictionary that will serve as the holder of all other documents
    database = {}

    # Using the retrieveTickers function from the tickerFetcher file, save the stocks' tickers in a list
    tickets = ticketsFetcher.retrieveTickets()

    # Create a dictionary with all stocks where each ticker is mapped to a dictionary
    # In this way, each ticker will become a document
    allStocks = {string: {} for string in tickets}

    # Loop through the tickers and submit them to the gather_info_basic function to collect the qualitative data
    # For each ticker, that is, stock, the id, name, sector, index and exchange are collected
    # Also, the Values and Ratios entities are created, but are still empty
    for ticket in tickets:
        company_name, sector, exchange = gatherInfoBasic.gather_info_basic(ticket)
        allStocks[ticket]['id'] = ticket
        allStocks[ticket]['name'] = company_name
        allStocks[ticket]['sector'] = sector
        allStocks[ticket]['index'] = 'S&P500'
        allStocks[ticket]['exchange'] = exchange
        allStocks[ticket]['values'] = {
            'close' : {},
            'volatility' : {},
            'volume' : {}
        }
        allStocks[ticket]['ratios'] = {
            'quarter' : [],
            'overallRisk' : [],
            'dividendYield' : [],
            'beta' : [],
            'peRatio' : [],
            'grossMargin' : [],
            'quickRatio' : [],
            'price-to-bookRatio' : []
        }

    # Create a dictionary with the desired exchanges' tickers mapped to a dictionary so each one can become a document
    # Afterward, use the exchangeRetriever function to retrieve the exchange, city and currency of each one
    # And, finally, create the structure for the Value entity
    exchanges = {'^NYA':{} , '^IXIC':{}}
    for k in exchanges.keys():
        city, currency, exchange = exchangeRetriever.exchangeRetriever(k)
        exchanges[k]['exchange'] = exchange
        exchanges[k]['city'] = city
        exchanges[k]['currency'] = currency
        exchanges[k]['values'] = {
            'close' : {},
            'volatility' : {},
            'volume' : {}
        }

    # Repeat the previous process for the indices
    indices = {'^GSPC':{} , '^DJI':{} , '^RUT':{} , '^W5000':{}}
    for k in indices.keys():
        currency, typeQuote, shortName = indexRetriever.indexRetriever(k)
        indices[k]['Name'] = shortName
        indices[k]['type'] = typeQuote
        indices[k]['currency'] = currency
        indices[k]['values'] = {
            'close' : {},
            'volatility' : {},
            'volume' : {}
        }

    # Join all previously created documents into the database dictionary to generate a big single document
    database['indices'] = indices
    database['exchanges'] = exchanges
    database['stocks'] = allStocks

    # Output the document to a JSON file
    with open('database1.json', 'w') as file:
        json.dump(database, file, indent=5)

    # Return the dictionary
    return database



