import sys
import os
sys.path.append(os.path.abspath('.'))
import pandas as pd
import numpy as np
from indicators import calculate as calc, load_data as load

import pandas as pd

def ema(ema_points=200, output='action'):
    a = load.binance_data_trade('BTC/USDT', '1m', output_dataframe=True)
    b = a.copy()
    b = b[['timestamp', 'close']]
    b['ema'] = b['close'].ewm(span=ema_points).mean()  # Calculate the exponential moving average
    b['ema_prev'] = b['ema'].shift()
    b['ema_diff'] = b['ema'] - b['ema_prev']
    b['current_direction'] = b['ema_diff'].apply(lambda x: 'positive' if x > 0 else ('flat' if x == 0 else 'negative'))
    b['previous_direction'] = b['current_direction'].shift()
    b['signal'] = 'hold'
    b.loc[(b['current_direction'] != b['previous_direction']) & (b['current_direction'] == 'positive'), 'signal'] = 'buy'
    b.loc[(b['current_direction'] != b['previous_direction']) & (b['current_direction'] == 'negative'), 'signal'] = 'sell'
    b = b.dropna()
    action = b.iloc[-1]['signal']
    if output == 'action':
        return action
    if output == 'dataframe':
        return b
    if output == 'df_action':
        return b.iloc[-1]

