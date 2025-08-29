import requests
import pandas as pd

def fetch_klines(symbol: str, interval: str = '1h', limit: int = 1000) -> pd.DataFrame:
    """
    Fetch candlestick (OHLCV) data from Binance for a given symbol.
    
    Parameters:
        symbol (str): e.g., 'BTCUSDT'
        interval (str): e.g., '1h', '15m', '1d'
        limit (int): Number of data points to fetch (max 1000)
    
    Returns:
        pd.DataFrame: Cleaned DataFrame with OHLCV and metadata
    """
    url = 'https://api.binance.com/api/v3/klines'
    params = {'symbol': symbol, 'interval': interval, 'limit': limit}
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    raw_data = response.json()
    columns = [
        'open_time', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'num_trades',
        'taker_buy_base_volume', 'taker_buy_quote_volume', 'ignore'
    ]
    
    df = pd.DataFrame(raw_data, columns=columns)
    
    # Convert timestamps and numeric columns
    df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
    df['close_time'] = pd.to_datetime(df['close_time'], unit='ms')
    numeric_cols = ['open', 'high', 'low', 'close', 'volume',
                    'quote_asset_volume', 'taker_buy_base_volume', 'taker_buy_quote_volume']
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
    
    return df

if __name__ == "__main__":
    df = fetch_klines('BTCUSDT')
    print(df.head())
    
    

def get_klines(symbol, interval='1h', limit=100):
    url = f'https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}'
    response = requests.get(url)
    data = response.json()
    
    import pandas as pd
    df = pd.DataFrame(data, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base_volume', 'taker_buy_quote_volume', 'ignore'
    ])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    df = df.astype(float)
    return df  
  
  
    
def get_order_book(symbol, limit=100):
    url = f'https://api.binance.com/api/v3/depth?symbol={symbol}&limit={limit}'
    response = requests.get(url)
    data = response.json()
    return data['bids'], data['asks']

def fetch_recent_trades(symbol, limit=500):
    url = f"https://api.binance.com/api/v3/trades?symbol={symbol}&limit={limit}"
    response = requests.get(url)
    trades = response.json()
    return trades


import requests

def get_binance_usdt_symbols():
    url = "https://api.binance.com/api/v3/exchangeInfo"
    response = requests.get(url)
    data = response.json()

    symbols = [
        s['symbol'] for s in data['symbols']
        if s['quoteAsset'] == 'USDT' and s['status'] == 'TRADING'
    ]
    return symbols
