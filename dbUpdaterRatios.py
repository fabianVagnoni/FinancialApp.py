# Updates DB with information about ratios
# That is, populate the Ratios Entity

# Import necessary libraries and files
import gatherInfoRatios
import json


# Define function to collect the information and update the database
def dbUpdaterRatios():

    # Read the database current JSON file
    with open('database1.json', 'r') as file:
        data = json.load(file)

    # Extract the stock's tickers
    keys = list(data['stocks'].keys())

    # For each ticker, use the gather_info_ratios function to extract the necessary ratios and save them in the Ratios Entity
    # related to the corresponding stock
    for k in keys:
        quarter, overallRisk, dividendYield, beta, peRatio, grossMargin, quickRatio, price_to_bookRatio = gatherInfoRatios.gather_info_ratios(k)

        # Step 2: Modify the Python object
        data['stocks'][k]['ratios']['quarter'].append(quarter)
        data['stocks'][k]['ratios']['overallRisk'].append(overallRisk)
        data['stocks'][k]['ratios']['dividendYield'].append(dividendYield)
        data['stocks'][k]['ratios']['beta'].append(beta)
        data['stocks'][k]['ratios']['peRatio'].append(peRatio)
        data['stocks'][k]['ratios']['grossMargin'].append(grossMargin)
        data['stocks'][k]['ratios']['quickRatio'].append(quickRatio)
        data['stocks'][k]['ratios']['price-to-bookRatio'].append(price_to_bookRatio)

    # Update the database
    with open('database2.json', 'w') as file:
        json.dump(data, file, indent=4)

    return data
