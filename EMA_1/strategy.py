import sys
import os
sys.path.append(os.path.abspath('.'))
import pandas as pd
import numpy as np
from indicators import calculate as calc, load_data as load

def ema(output='action'):
    a = load.binance_data_trade('BTC/USDT','1m',output_dataframe=True)
    b = calc.ema_ribbon(a,points=[20,55])
    c = b.copy()
    c = c[['timestamp','close','volume','20_ema','55_ema']]
    c['55>20'] = c['55_ema'] > c['20_ema']
    c['55>20_prev'] = c['55>20'].shift()
    c['signal'] = 'hold'
    c.loc[(c['55>20'] == True) & (c['55>20_prev'] == False), 'signal'] = 'buy'
    c.loc[(c['55>20'] == False) & (c['55>20_prev'] == True), 'signal'] = 'sell'
    action = c.iloc[-1]['signal']
    if output == 'action':
        return action
    if output == 'dataframe':
        return c
    if output == 'df_action':
        return c.iloc[-1]
