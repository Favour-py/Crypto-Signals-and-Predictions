# Crypto Signal & Prediction API

This FastAPI-based application analyzes real-time market data from Binance and generates trading signals for over 245 USDT trading pairs. It uses technical indicators and order book dynamics to determine whether to **buy**, **sell**, **hold**, or **exit** a position.

## Features

- Fetches live OHLCV, order book, and trade data from Binance
- Calculates indicators: RSI, MACD, EMA9, EMA21, ADX, Bollinger Bands, and Volume
- Scores bullish and bearish conditions using a 6-point system
- Returns actionable signals with strength and condition breakdown
- Supports over 245 USDT trading pairs dynamically

## Signal Logic

### Buy Signal
Triggered when:
- At least 3 bullish conditions are true
- buyScore > sellScore

**Strength** = `(buyScore / 6) * 100`

### Sell Signal
Triggered when:
- At least 3 bearish conditions are true
- sellScore > buyScore

**Strength** = `(sellScore / 6) * 100`

### Hold Signal
Triggered when:
- RSI is between 40–60
- ADX < 20

### Exit Signal
Triggered when:
- Previous signal was Buy and now sellScore ≥ 3
- Previous signal was Sell and now buyScore ≥ 3
- ADX < 20

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name

## Run the FastAPI server

uvicorn main:app --reload



