import ta

def generate_signals(df, rsi_buy=35, rsi_sell=65, ema_period=20):
    df['sma'] = df['close'].rolling(window=ema_period).mean()
    df['rsi'] = ta.momentum.RSIIndicator(close=df['close']).rsi()
    macd = ta.trend.MACD(close=df['close'])
    df['macd'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()

    df['buy_signal'] = (
        (df['rsi'] < rsi_buy) &
        (df['macd'] > df['macd_signal']) &
        (df['close'] < df['sma'])
    )

    df['sell_signal'] = (
        (df['rsi'] > rsi_sell) &
        (df['macd'] < df['macd_signal']) &
        (df['close'] > df['sma'])
    )

    return df


def predict_signal(df, bids, asks, trades):
    # Order book imbalance
    bid_volume = sum(float(b[1]) for b in bids)
    ask_volume = sum(float(a[1]) for a in asks)
    order_book_bias = bid_volume - ask_volume

    # Trade momentum
    buyer_trades = sum(1 for t in trades if not t['isBuyerMaker'])
    seller_trades = sum(1 for t in trades if t['isBuyerMaker'])
    trade_bias = buyer_trades - seller_trades

    # Latest row of indicators
    latest = df.iloc[-1]
    rsi = latest['rsi']
    macd = latest['macd']
    macd_signal = latest['macd_signal']

    # Signal logic
    if rsi < 35 and macd > macd_signal and order_book_bias > 0 and trade_bias > 0:
        return 'buy'
    elif rsi > 65 and macd < macd_signal and order_book_bias < 0 and trade_bias < 0:
        return 'sell'
    elif abs(order_book_bias) < 1000 and abs(trade_bias) < 10:
        return 'hold'
    else:
        return 'exit'
    
