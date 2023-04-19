import sys
import os
sys.path.append(os.path.abspath('.'))
import time
import trade as tr
import strategy as stg

action = 'buy'
bal = tr.get_balance('USDT')
amount = bal*0.5
tr.execute_trade('BTC/USDT', action, amount)
