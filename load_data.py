import ccxt
import pandas as pd
import numpy as np
from datetime import datetime

def np_to_df(input_array,columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']):
    data = pd.DataFrame(input_array, columns=columns)
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
    return data

def binance_data(trading_pair, interval, start_date, end_date=None, output_dataframe=False, export_path=None):
    exchange = ccxt.binance({
        'rateLimit': 1200,
        'enableRateLimit': True,
    })

    # Convert start date and end date to timestamps
    start_timestamp = exchange.parse8601(start_date)
    if end_date:
        end_timestamp = exchange.parse8601(end_date)
    else:
        end_timestamp = exchange.milliseconds()

    # Define the timeframe
    timeframe = f'{interval}m'

    # Initialize an empty list to store data
    data = []

    # Load historical OHLCV data using pagination
    while start_timestamp < end_timestamp:
        try:
            ohlcv = exchange.fetch_ohlcv(trading_pair, timeframe, since=start_timestamp)
            if not ohlcv:
                break

            # Update the start timestamp for the next iteration
            start_timestamp = ohlcv[-1][0] + exchange.parse_timeframe(timeframe) * 1000

            # Append the data to the list
            data.extend(ohlcv)

        except ccxt.NetworkError as e:
            print(f'NetworkError: {e}')
            break

        except ccxt.BaseError as e:
            print(f'BaseError: {e}')
            break

    # Convert the list to a NumPy array
    data = np.array(data)

    # If output_dataframe is True, convert the data to a pandas DataFrame
    if output_dataframe:
        data = np_to_df(data)
        if export_path is not None:
            data.to_csv('pd_' + export_path + trading_pair + '.csv', index=False)
    if export_path is not None:
        np.savetxt('np_', export_path + trading_pair + '.csv', data, delimiter=',')
    return data

def local_data(file_path, output_dataframe=False):
    # Load data from CSV file
    data = np.genfromtxt(file_path, delimiter=',', skip_header=1)

    # Return data as a NumPy array or a Pandas DataFrame
    if output_dataframe:
        #columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        columns = ['close', 'close_pct_change', '5_min_EMA', '15_min_EMA', '25_min_EMA', '35_min_EMA', '45_min_EMA', '55_min_EMA', '200_min_EMA', 'RSI']
        return pd.DataFrame(data, columns=columns)
    else:
        return data