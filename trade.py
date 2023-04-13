import ccxt
import config

api_key = config.api_key
api_secret = config.api_secret

binance = ccxt.binance({
    'apiKey': api_key,
    'secret': api_secret,
})

def get_balance(symbol):
    symbol = symbol.upper()
    balance = binance.fetch_balance()
    return balance[symbol]['free']

def get_price(symbol):
    """
    Get the current price of a trading pair.

    :param symbol: The trading pair symbol, e.g. 'BTC/USDT'
    :return: The current price as a float
    """
    ticker = exchange.fetch_ticker(symbol)
    return float(ticker['ask'])

def execute_trade(symbol, trade_type, amount):
    symbol = symbol.upper()
    trade_type = trade_type.lower()

    if trade_type not in ['buy', 'hold', 'sell']:
        print("Invalid trade type. Use 'buy' or 'sell'.")
        return

    try:
        if trade_type == 'buy':
            order = binance.create_market_buy_order(symbol, amount)
        elif trade_type == 'sell':
            order = binance.create_market_sell_order(symbol, amount)
        elif trade_type == 'hold':
            order = 'Holding'
        if trade_type != 'hold':
            print(f"Successfully executed {trade_type} order for {amount} {symbol}:")
        else:
            print(f"{trade_type}ing")
        print(order)
    except Exception as e:
        print(f"Error executing {trade_type} order for {amount} {symbol}:")
        print(e)