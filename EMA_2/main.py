import sys
import os
sys.path.append(os.path.abspath('.'))
import math
import time
import trade as tr
import strategy as stg

while True:
    action = stg.ema()
    print(stg.ema(200,'df_action'))
    print(action)

    if action == 'buy':
        bal = tr.get_balance('USDT')
        print(bal, 'USDT')

        # Get the current price of BTC/USDT
        btc_usdt_price = tr.get_price('BTC/USDT')

        # Calculate the amount of BTC you can buy with 95% of your available USDT balance
        amount = math.floor(bal) / btc_usdt_price

    elif action == 'sell':
        bal = tr.get_balance('BTC')
        print(bal, 'BTC')

        # Calculate the amount of BTC to sell, which is 95% of your available BTC balance
        amount = bal * 0.95

    elif action == 'hold':
        amount = 0

    tr.execute_trade('BTC/USDT', action, amount)

    # Pause the loop for 60 seconds (1 minute) before running the next iteration
    time.sleep(60)

