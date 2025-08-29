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


def predict_signal(symbol, df, bids, asks, trades):
    # Order book imbalance
    bid_volume = sum(float(b[1]) for b in bids)
    ask_volume = sum(float(a[1]) for a in asks)
    order_book_bias = bid_volume - ask_volume

    # Trade momentum
    buyer_trades = sum(1 for t in trades if not t['isBuyerMaker'])
    seller_trades = sum(1 for t in trades if t['isBuyerMaker'])
    trade_bias = buyer_trades - seller_trades
 

# RSI
    rsi = ta.momentum.RSIIndicator(df['close']).rsi()

    # MACD
    macd = ta.trend.MACD(df['close'])
    macd_line = macd.macd()
    macd_signal = macd.macd_signal()

    # EMA
    ema9 = ta.trend.EMAIndicator(df['close'], window=9).ema_indicator()
    ema21 = ta.trend.EMAIndicator(df['close'], window=21).ema_indicator()

    # ADX, PDI, MDI
    adx = ta.trend.ADXIndicator(df['high'], df['low'], df['close'])
    adx_value = adx.adx()
    pdi = adx.adx_pos()
    mdi = adx.adx_neg()

    # Bollinger Bands
    bb = ta.volatility.BollingerBands(df['close'])
    bb_lower = bb.bollinger_lband()
    bb_upper = bb.bollinger_hband()

    # Volume spike (compare current volume to moving average)
    volume_spike = df['volume'].iloc[-1] > df['volume'].rolling(window=20).mean().iloc[-1]


    buyScore = 0
    sellScore = 0
    conditions_met = []

    # BUY Conditions
    if rsi.iloc[-1] < 30:
        buyScore += 1
        conditions_met.append("RSI < 30")

    if macd_line.iloc[-1] > macd_signal.iloc[-1] and macd_line.iloc[-1] < 0:
        buyScore += 1
        conditions_met.append("MACD bullish crossover below zero")

    if ema9.iloc[-1] > ema21.iloc[-1]:
        buyScore += 1
        conditions_met.append("EMA9 > EMA21")

    if adx_value.iloc[-1] > 20 and pdi.iloc[-1] > mdi.iloc[-1]:
        buyScore += 1
        conditions_met.append("ADX > 20 and PDI > MDI")

    if rsi.iloc[-1] < 30 and macd_line.iloc[-1] > macd_signal.iloc[-1]:
        buyScore += 1
        conditions_met.append("RSI < 30 + MACD crossover")

    if df['close'].iloc[-1] < bb_lower.iloc[-1] and rsi.iloc[-1] < 40 and volume_spike:
        buyScore += 1
        conditions_met.append("Near Bollinger lower + RSI < 40 + volume spike")

    # SELL Conditions
    if rsi.iloc[-1] > 65:
        sellScore += 1
        conditions_met.append("RSI > 65")

    if macd_line.iloc[-1] < macd_signal.iloc[-1] and macd_line.iloc[-1] > 0:
        sellScore += 1
        conditions_met.append("MACD bearish crossover above zero")

    if ema9.iloc[-1] < ema21.iloc[-1]:
        sellScore += 1
        conditions_met.append("EMA9 < EMA21")

    if adx_value.iloc[-1] > 20 and mdi.iloc[-1] > pdi.iloc[-1]:
        sellScore += 1
        conditions_met.append("ADX > 20 and MDI > PDI")

    if rsi.iloc[-1] > 70 and macd_line.iloc[-1] < macd_signal.iloc[-1]:
        sellScore += 1
        conditions_met.append("RSI > 70 + MACD crossover")

    if df['close'].iloc[-1] > bb_upper.iloc[-1] and rsi.iloc[-1] > 60 and volume_spike:
        sellScore += 1
        conditions_met.append("Near Bollinger upper + RSI > 60 + volume spike")


    strength = (buyScore / 6) * 100 if buyScore > sellScore else (sellScore / 6) * 100

    if buyScore >= 3 and buyScore > sellScore:
        signal = "buy"
    elif sellScore >= 3 and sellScore > buyScore:
        signal = "sell"
    elif 40 <= rsi.iloc[-1] <= 60 and adx_value.iloc[-1] < 20:
        signal = "hold"
    elif adx_value.iloc[-1] < 20 or abs(buyScore - sellScore) >= 3:
        signal = "exit"
    else:
        signal = "hold"
        
        
    return {
    "symbol": symbol,
    "signal": signal,
    "buyScore": buyScore,
    "sellScore": sellScore,
    "strength": round(strength, 2),
    "conditionsMet": conditions_met
}

