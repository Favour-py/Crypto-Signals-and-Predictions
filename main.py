from fastapi import FastAPI
from data_fetch import fetch_klines, get_klines, get_order_book, fetch_recent_trades
from indicators import calculate_indicators
from signals import predict_signal, generate_signals
from backtest import backtest_strategy, calculate_metrics
import pandas as pd
import time
import datetime

app = FastAPI()

# ✅ FastAPI endpoint
@app.get("/signal/{symbol}")
def get_signal(symbol: str):
    try:
        df = fetch_klines(symbol)
        df = calculate_indicators(df)
        bids, asks = get_order_book(symbol)
        trades = fetch_recent_trades(symbol)
        signal = predict_signal(df, bids, asks, trades)
        return {"symbol": symbol, "signal": signal}
    except Exception as e:
        return {"error": str(e)}

# ✅ Backtesting loop
symbol = 'BTCUSDT'  # Default symbol for testing
df = fetch_klines(symbol)
df = calculate_indicators(df)

for rsi_buy, rsi_sell in [(35, 65), (40, 60), (45, 55)]:
    df_signals = generate_signals(df.copy(), rsi_buy=rsi_buy, rsi_sell=rsi_sell)
    trades, final_balance = backtest_strategy(df_signals, rsi_buy=rsi_buy, rsi_sell=rsi_sell)
    metrics = calculate_metrics(trades, initial_balance=10000)
    print(f"\nRSI Buy: {rsi_buy}, RSI Sell: {rsi_sell}")
    print(f"Final Balance: ${final_balance:.2f}")
    for k, v in metrics.items():
        print(f"{k}: {v}")

# ✅ Live signal loop
from data_fetch import get_binance_usdt_symbols

symbols = get_binance_usdt_symbols()
  # Add more as needed

while True:
    current_time = datetime.datetime.now()

    for symbol in symbols:
        try:
            df = get_klines(symbol)
            df = calculate_indicators(df)
            bids, asks = get_order_book(symbol)
            trades = fetch_recent_trades(symbol)
            signal = predict_signal(df, bids, asks, trades)
            print(f"{symbol}: {signal}")
        except Exception as e:
            print(f"Error with {symbol}: {e}")

    if current_time.minute % 10 == 0:
        for symbol in symbols:
            print(f"{symbol}: Hold/Exit check")

    time.sleep(0.1)
