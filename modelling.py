# Script that takes a security and a time horizon and makes a prediction using an ARIMA model from those
# Afterwards plots the prediction and saves the plot
import sys

from pmdarima.arima import auto_arima
import json
import os
import matplotlib.pyplot as plt
import pandas as pd
from prophet import Prophet


def a_arima(security, h):
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

    # Take the series of values needed and save it as a list
    name = data[category][security]['name']
    data_series_list = list(data[category][security]['values']['close'].items())
    data_series = pd.DataFrame(data_series_list[len(data_series_list)-365*5:], columns=['ds', 'y'])#list(data_series.values())
    print(data_series)

    # Create the ARIMA model
    # The auto ARIMA takes care of the hyperparams pdq
    # The seasonal hyperparams PDQ are not used because we assume stock prices are not seasonal
    # (This assumption is true for almost all stocks, if not all)
    #model = auto_arima(data_series, start_p=0, start_q=0, start_P=0, start_Q=0, m=1,
    #                   suppress_warnings=True, n_fits=50)

    # Create Prophet model and fit it to the data
    # Model automatically handles piecewise regression trend
    model = Prophet()
    model.fit(data_series)

    # Uncomment to see summary
    # model.summary()

    # Make the prediction and round it
    #prediction = model.predict(n_periods=h)
    #prediction = [round(i , 2) for i in prediction]
    future = model.make_future_dataframe(periods=h)
    prediction = model.predict(future)
    #print(prediction)
    #prediction = [round(i , 2) for i in prediction]

    # Join the prediction with the last five years of data
    #all_data = data_series[-365*5:] + prediction
    #indices = range(0 , len(all_data))

    # Convert to pandas DataFrame for easier plotting
    #data = pd.DataFrame({'Values' : all_data}, index=indices)len(data_series_list)-365*3
    #print(len(prediction.index))
    #print(prediction['yhat'].iloc[len(data_series_list):len(data_series_list)+h])
    print(prediction['ds'])

    # Plot the actual and predicted values in different colors
    plt.clf()
    plt.plot(prediction['ds'].iloc[0:len(prediction.index)-h] , prediction['yhat'].iloc[0:len(prediction.index)-h], label='Actual', lw=1)
    plt.plot(prediction['ds'].iloc[len(prediction.index)-h:len(prediction.index)] , prediction['yhat'].iloc[len(prediction.index)-h:len(prediction.index)], color='red', label='Predictions', lw=1)
    plt.xlabel('Time')
    plt.ylabel('Price (in $)')
    plt.title(f'{name}: Real Data vs Predictions')
    plt.legend()
    plt.tight_layout()

    # Save the plot so the app can retrieve it
    # If the user creates other prediction plot, this one will be overwritten
    path = os.getcwd()+f'\preds{security}.png'
    for file in os.listdir('.'):
        if 'preds' in file:
            os.remove(file)
    plt.savefig(path)

    return str(path)



