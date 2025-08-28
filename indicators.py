import pandas as pd
import ta


def add_indicators(df):
    # Add RSI
    df['rsi'] = ta.momentum.RSIIndicator(close=df['close']).rsi()
    
    # Add 20-period SMA
    df['sma_20'] = ta.trend.SMAIndicator(close=df['close'], window=20).sma_indicator()
    
    # Add MACD
    macd = ta.trend.MACD(close=df['close'])
    df['macd'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()
    
    # Add volatility (rolling std dev)
    df['volatility'] = df['close'].rolling(window=20).std()
    
    return df

# df = fetch_klines('BTCUSDT')
# df = add_indicators(df)
# print(df.tail())



def calculate_indicators(df):
    import pandas as pd

    # RSI
    delta = df['close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df['rsi'] = 100 - (100 / (1 + rs))

    # MACD
    ema12 = df['close'].ewm(span=12, adjust=False).mean()
    ema26 = df['close'].ewm(span=26, adjust=False).mean()
    df['macd'] = ema12 - ema26
    df['macd_signal'] = df['macd'].ewm(span=9, adjust=False).mean()

    return df
