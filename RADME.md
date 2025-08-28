# 📈 Crypto Signal & Prediction API

This project analyzes crypto market data using technical indicators and generates actionable trading signals (Buy, Sell, Hold, Exit). It also includes a backtesting engine to evaluate strategy performance and exposes a FastAPI endpoint for real-time signal access.

---

## 🚀 Features

- Fetches live candlestick data from Binance
- Calculates RSI, MACD, SMA, and volatility indicators
- Generates trading signals based on market bias and indicator thresholds
- Backtests strategy performance across multiple RSI configurations
- Exposes a `/signal/{symbol}` API endpoint for real-time signal access
- Includes a live loop for continuous signal monitoring

---

## 🛠 Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
