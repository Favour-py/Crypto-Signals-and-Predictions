from signals import generate_signals, predict_signal
from data_fetch import fetch_klines, get_order_book, fetch_recent_trades
import requests

def get_binance_usdt_symbols(limit=245):
    """
    Fetches USDT trading pairs from Binance and returns the top `limit` symbols.
    """
    url = "https://api.binance.com/api/v3/ticker/price"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        symbols = [item['symbol'] for item in data if item['symbol'].endswith('USDT')]
        return symbols[:limit]
    except Exception as e:
        print(f"Error fetching symbols: {e}")
        return []



def generate_signals_for_tokens():
    symbols = get_binance_usdt_symbols()
    results = []

    for symbol in symbols:
        df = fetch_klines(symbol)  # from data_fetch.py
        df = generate_signals(df, rsi_buy=35, rsi_sell=65)

        bids, asks = get_order_book(symbol)
        trades = fetch_recent_trades(symbol)

        signal = predict_signal(df, bids, asks, trades)

        print(f"{symbol}: {signal}")

    import json

    with open("signals_245_tokens.json", "w") as f:
        json.dump(results, f, indent=2)

    return results

if __name__ == "__main__":
    generate_signals_for_tokens()
