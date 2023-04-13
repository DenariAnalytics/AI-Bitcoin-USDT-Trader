import ccxt
import numpy as np
import pandas as pd
import tensorflow as tf
from datetime import datetime
from time import sleep

from indicators import calculate as calc, load_data as load
import preprocess_data
import setup 
import joblib
import config

# Load the scaler from the file
scaler = joblib.load('scaler.pkl')

# Load your API keys and create an instance of the Binance client
api_key = config.api_key
api_secret = config.api_secret

client = ccxt.binance({
    'apiKey': api_key,
    'secret': api_secret,
    'rateLimit': 1200,
    'enableRateLimit': True,
})

# Load the saved model
model = tf.keras.models.load_model('btc-usdt_trading_model.h5')

# Define a function to fetch new data and preprocess it
# Define a function to fetch new data and preprocess it
def fetch_and_preprocess_data(trading_pair, interval):
    end_date = datetime.now()
    start_date = end_date - pd.DateOffset(minutes=300)  # Fetch data for the last 300 minutes

    data = load_data.binance_data(trading_pair, interval, start_date.isoformat(), end_date.isoformat(), output_dataframe=True)
    data = preprocess_data.process(data)
    
    # Keep only the expected columns
    expected_columns = ['close', 'close_pct_change', '5_min_EMA', '15_min_EMA', '25_min_EMA', '35_min_EMA', '45_min_EMA', '55_min_EMA', '200_min_EMA', 'RSI']
    data = data[expected_columns]
    
    return data



# Define a function to predict and generate trading signals
def generate_signals(data):
    # Scale and create sequences
    data_scaled = data.copy()
    data_scaled.iloc[:, 0] = scaler.transform(data.iloc[:, 0].to_numpy().reshape(-1, 1)).flatten()
    X, _ = setup.create_sequences(data_scaled.to_numpy())

    # Make predictions
    y_pred = model.predict(X[-1:])
    return y_pred[0][0]  # Return the signal value directly



def get_balance(asset):
    balance = client.fetch_balance()
    asset_balance = float(balance[asset]['free'])
    return asset_balance

# Define a function to execute trades based on the generated signals
def execute_trade(signal):
    base_currency = 'BTC'
    quote_currency = 'USDT'
    symbol = f'{base_currency}/{quote_currency}'
    
    base_balance = get_balance(base_currency)
    quote_balance = get_balance(quote_currency)
    
    # Retrieve the current ticker price
    ticker = client.fetch_ticker(symbol)
    current_price = ticker['ask']

    trade_amount = 0.95  # Define the trade amount (e.g., 1% of the quote balance)

    if signal > 0 and quote_balance > 0:
        # Buy logic
        order_amount = quote_balance * trade_amount / current_price
        order = client.create_market_buy_order(symbol, order_amount)
        print(f"Buy order executed: {order}")
    elif signal < 0 and base_balance > 0:
        # Sell logic
        order_amount = base_balance * trade_amount
        order = client.create_market_sell_order(symbol, order_amount)
        print(f"Sell order executed: {order}")


# Implement a loop to periodically fetch data, generate signals, and execute trades
trading_pair = 'BTC/USDT'
interval = '1m'  # 1 minutes

while True:
    try:
        data = fetch_and_preprocess_data(trading_pair, interval)
        y_pred = generate_signals(data)
        trading_signal = setup.calculate_trading_signals(y_pred[0, 0], data['close'].values[-1])
        execute_trade(trading_signal)
        sleep(60)  # Sleep for the duration of the interval (in seconds)
    except Exception as e:
        print(f'Error: {e}')
