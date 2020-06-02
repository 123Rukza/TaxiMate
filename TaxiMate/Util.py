# Additional utilities required
# Imports
import pandas as pd


class Util:

    # Transform data to conform with prophet requirements
    def transform_data(borough):
        # Get only the required columns
        data = borough[['DateTime', 'Demand', 'Temperature', 'Visibility', 'SeaLevelPressure', 'LiquidPrec1',
                        'LiquidPrec6', 'LiquidPrec24', 'SnowDepth', 'IsHoliday']].copy()
        # Convert date column to date time objects
        data['DateTime'] = pd.to_datetime(data['DateTime'])
        # Renaming in shorthand format for prophet
        data.columns = ['ds', 'y', 'temp', 'vis', 'slp', 'lp1', 'lp6', 'lp24', 'snow', 'IsHoliday']
        # Return data with reset index to aboid null values in index
        return data.reset_index(drop=True)

    # Find the unique dates which are holidays from the dataset
    @staticmethod
    def get_holidays(data):
        # Get holidays where is holiday is true
        holiday_list = data.loc[data['IsHoliday'] == 1]
        # Drop 23 values and select only 00:00:00 value and set to prophet format
        holidays = pd.DataFrame({
            'holiday': 'Unnamed_Holidays',
            'ds': pd.to_datetime(holiday_list['ds'].dt.floor('d').drop_duplicates().values),
            'lower_window': 0,
            'upper_window': 1,
        })
        # Return holidays
        return holidays

    # Format output
    @staticmethod
    def format_output(forecast):
        # Formatting values
        output = pd.DataFrame({'DateAndTime': forecast[:, 0]})
        output['Demand'] = forecast[:, 1]
        output['DateAndTime'] = pd.to_datetime(output['DateAndTime'], unit='s')

        # Convert to proper JSON format for the front end
        json_str = output.to_json(date_format='iso', orient='records', lines=True)
        json_str = '[' + json_str.replace('}\n{', '},{') + ']'
        return json_str
