import sys
import os
sys.path.append(os.path.abspath('..'))

import numpy as np
import pandas as pd

import calculate as calc

#Process
def process(input_data):
    data = input_data.copy()
    # Convert timestamp to datetime object
    data['timestamp'] = data['timestamp'].apply(lambda x: pd.Timestamp(x, unit='ms', tz='UTC'))

    # Calculate EMA Ribbon
    data = calc.ema_ribbon(data)
    data = calc.rsi(data)

    # Calculate the percentage change in closing price
    data['close_pct_change'] = data['close'].pct_change()

    # Drop any rows with NaN values
    data.dropna(inplace=True)

    # Select the columns you want to use as input features for your LSTM model
    feature_columns = list(data.columns)
    feature_data = data[feature_columns]

    return feature_data
