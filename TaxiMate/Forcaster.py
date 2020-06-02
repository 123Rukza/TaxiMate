# Prophet forecaster module
# Imports
from fbprophet import Prophet


class Forcaster:

    # Create Prophet model and add additional regressors
    @staticmethod
    def create_model(names, holidays):
        # Create model with linear growth logistic is slower and less accurate, include holidays
        m = Prophet(growth='linear', changepoint_prior_scale=0.01, holidays=holidays)

        # Add regressors in a loop with column name
        for i in range(len(names)):
            if 2 < i < int(len(names)) - 1:
                m.add_regressor(names[i])
        # return the model
        return m

    # Create future data frame to receive forecast
    @staticmethod
    def create_future(data, m):
        # Create future data frame to receive 24 predictions at Hourly frequency
        future = m.make_future_dataframe(periods=24, freq='H')
        names = list(data.columns.values)

        # Add labels and values for regressors
        for i in range(len(names)):
            if 2 < i < int(len(names)) - 1:
                future[names[i]] = data.iloc[:, i]

        # Return future object
        return future
