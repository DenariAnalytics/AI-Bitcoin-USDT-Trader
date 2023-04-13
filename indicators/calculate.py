def ema(input_data, points=5):
    data = input_data.copy()
    data[f'{points}_ema'] = data['close'].ewm(span=points).mean()
    return data

def ema_ribbon(input_data, points=[5, 15, 25, 35, 45, 55, 200], column_names=False):
    data = input_data.copy()
    columns = [f'{point}_ema' for point in points]
    for point, column_name in zip(points, columns):
        data[column_name] = data['close'].ewm(span=point).mean()
    if column_names:
        return columns
    return data

def ma(input_data, points=5):
    data = input_data.copy()
    data[f'{points}_ma'] = data['close'].rolling(window=points).mean()
    return data

def rsi(input_data, period=14, column='close'):
    data = input_data.copy()
    delta = data[column].diff()
    gain, loss = delta.copy(), delta.copy()
    
    gain[gain < 0] = 0
    loss[loss > 0] = 0
    loss = abs(loss)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    # Add the RSI column to the input DataFrame
    data['RSI'] = rsi
    data.dropna(inplace=True)
    return data