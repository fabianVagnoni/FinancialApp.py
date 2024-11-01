# Updates the Values Entity with daily data

# Import necessary files and libraries
import gatherInfoValue
import json

# Define the function that will retrieve the values and add them to the Values Entity
def dailyUpdater():
    # Open the DB JSON file
    with open('database3.json', 'r') as file:
        data = json.load(file)

    # Extract the keys of the database, that is, Stocks, Indices and Exchanges
    keysDB = list(data.keys())

    # Loop over all documents of each key, that is, all tickers in stocks, all
    # tickers in indices and all tickers in exchanges
    for key in keysDB:
        for keySec in data[key].keys():
            # For each ticker, extract the attributes of the Values Entity using the
            # gatherInfoValue function with the parameter daily set to True so only
            # information corresponding to the last 24h is collected
            tradingDates, volatility, volume, close = gatherInfoValue.gatherInfoValue(keySec , daily=True)

            # Checking that actually information was available
            if close != None:
                # If there was information, map a new observation of close and one of volume
                # to the data
                for i in range(len(tradingDates)):
                    data[key][keySec]['values']['close'][tradingDates[i]] = close[i]
                    data[key][keySec]['values']['volume'][tradingDates[i]] = volume[i]

    # Save the changes in the database
    with open('database3.json', 'w') as file:
        json.dump(data, file, indent=4)

    return data


db = dailyUpdater()