# Given a timeSpan and a ticker, check that these are in the DB and plot them if possible


# Import all necessary libraries
import json
import matplotlib.pyplot as plt
import pandas as pd
import os


# Define the function that will check for errors and plot if possible
def returnCalc(security , timespan):

    # Open the database
    with open('database3.json', 'r') as file:
        data = json.load(file)

    # Extract from the database all keys from the Indices, Exchanges and Stocks documents
    # These keys are the tickers
    indices = list(data['indices'].keys())
    exchanges = list(data['exchanges'].keys())
    stocks = list(data['stocks'].keys())

    # Check in which document the inputted ticker is and create a variable category to
    # store this information. The order is relevant: since the stock document has the larger
    # number of tickers, leave it to the end, so no resources are spent on avoidable tasks
    if security in indices:
        category = 'indices'
    elif security in exchanges:
        category = 'exchanges'
    elif security in stocks:
        category = 'stocks'
    # If the ticker was in no document, return 'stockError'
    # This error will be managed by the submit function
    else:
        return 'stockError'

    # Extract the security's closing prices from the database and the corresponding dates
    span = data[category][security]['values']['close']
    if not span:
        return 'stockError'
    datesAll = pd.to_datetime(list(span.keys()))

    # Split the inputted timeSpan into two separate dates and convert them into datetime objects
    d1 , d2 = timespan.split(',')
    d1 , d2 = pd.to_datetime(d1) , pd.to_datetime(d2)

    # Check that these timeSpan variables are in chronological order
    # If not, return an error that will be handled by the submit function
    if d1 > d2:
        return 'dateError'

    # Check if the first date of the timeSpan is in the available dates corresponding to the
    # security's closing prices
    if d1 not in datesAll:
        # If this date is not in the available dates, create another checking variable
        checker = True

        # Loop over all available dates and check if there is any one that is at most
        # three days apart from the inputted date. This is done because the user might
        # have inputted a holiday or weekend date.
        for d in datesAll:
            if abs((d - d1).days) <= 3:
                # In case the user indeed inputted a date that was not available due to it
                # being a holiday or weekend, change the initial date of the timeSpan to the
                # closest one and convert checker to false
                d1 = d
                checker = False
                break
        # If after the looping checker is still true and, hence, no date was found that fell
        # three or less days away from the inputted date, return an error
        if checker:
            return 'dateError'

    # Check if the second date of the timeSpan is in the available dates corresponding to the
    # security's closing prices
    if d2 not in datesAll:
        # If this date is not in the available dates, create another checking variable
        checker = True

        # Loop over all available dates and check if there is any one that is at most
        # three days apart from the inputted date. This is done because the user might
        # have inputted a holiday or weekend date.
        for d in datesAll:
            if abs((d - d2).days) <= 3:
                # In case the user indeed inputted a date that was not available due to it
                # being a holiday or weekend, change the final date of the timeSpan to the
                # closest one and convert checker to false
                d2 = d
                checker = False
                break
        # If after the looping checker is still true and, hence, no date was found that fell
        # three or less days away from the inputted date, return an error
        if checker:
            return 'dateError'

    # Extract the values corresponding to the initial and final dates
    v1 = span[d1.strftime('%Y-%m-%d')]
    print(v1)
    v2 = span[d2.strftime('%Y-%m-%d')]
    print(v2)

    # Calculate return
    return round(100 * (v2 - v1)/v1 , 2)
