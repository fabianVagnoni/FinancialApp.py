# Updates the database with historical values of the stock
# This data ought to be updated daily

# Import necessary libraries and files
import json
import gatherInfoValue

# Define the function to update the database
def dbUpdaterHistorical():

    # Open the database
    with open('database2.json', 'r') as file:
        data = json.load(file)

    # Extract the keys of the database, that is, Stocks, Indices and Exchanges
    keysDB = list(data.keys())

    # Loop over the tickers of each key
    # That is, loop over all documents stored in stocks, all documents stored in indices
    # and all documents stored in exchanges
    for key in keysDB:
        for keySec in data[key].keys():

            # For each ticker, extract the attributes of the Values Entity using gatherInfoValue
            tradingDates, volatility, volume, close = gatherInfoValue.gatherInfoValue(keySec)

            # Check if volatility exists. If it does not, no other attribute was collected, since
            # the historical information of the security was None
            if volatility:
                # Saving the attributes
                # Volatility is mapped to the timespan that it covers
                data[key][keySec]['values']['volatility'][f'({tradingDates[0]}:{tradingDates[-1]})'] = volatility

                # close's and volume's values will be mapped to the date in which they happened,
                # so, loop over the dates and for each one extract the corresponding close and volume
                # value and map them together
                for i in range(len(tradingDates)):
                    data[key][keySec]['values']['close'][tradingDates[i]] = close[i]
                    data[key][keySec]['values']['volume'][tradingDates[i]] = volume[i]

    # With all the information, create a new database version
    with open('database3.json', 'w') as file:
        json.dump(data, file, indent=4)

    return data

