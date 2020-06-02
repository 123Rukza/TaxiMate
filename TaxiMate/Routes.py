# Routing management module for flask
# Imports
from TaxiMate.Forcaster import Forcaster
from TaxiMate.Util import Util
from TaxiMate import app
import pandas as pd
from flask import request


# Test method to verify the status of API
@app.route("/TaxiMate/Validate", methods=['GET'])
def validate():
    # Return functioning response
    return 'TaxiMate Python API Running'


# Main method to calculate forecast using given JSON data
@app.route("/TaxiMate/Predict", methods=['GET', 'POST'])
def predict():
    # Get dataset from JSON request
    dataset = pd.DataFrame(request.json)
    # Transform dataset in to prophet format
    data = Util.transform_data(dataset).reset_index(drop=True)
    # Get holidays from transformed data
    holidays = Util.get_holidays(data)

    # Create prophet forecaster model with regressors
    m = Forcaster.create_model(list(data.columns.values), holidays)
    # Split data to train
    data_train = data[:int(len(data) - 24)].reset_index(drop=True)
    m.fit(data_train)

    # Create future dataframe to receive forecast
    future = Forcaster.create_future(data, m)

    # Get forecast details
    forecast = m.predict(future)
    # Format output
    output = Util.format_output(forecast[['ds', 'yhat']][int(len(forecast)) - 24:].values)
    return output


# Analytics method to check prediction summary etc
@app.route("/TaxiMate/Analytics")
def analytics():
    dataset = pd.DataFrame(request.get_json())
    print(dataset.head())
