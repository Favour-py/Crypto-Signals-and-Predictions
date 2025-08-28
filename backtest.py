import numpy as np
from signals import generate_signals

def backtest_strategy(df, rsi_buy=35, rsi_sell=65, initial_balance=10000):
    df = generate_signals(df, rsi_buy=rsi_buy, rsi_sell=rsi_sell)
    balance = initial_balance
    position = 0
    entry_price = 0
    trades = []

    for i in range(len(df)):
        row = df.iloc[i]

        if row['buy_signal'] and position == 0:
            position = balance / row['close']
            entry_price = row['close']
            balance = 0
            trades.append({'type': 'buy', 'price': entry_price, 'time': row['open_time']})

        elif row['sell_signal'] and position > 0:
            balance = position * row['close']
            exit_price = row['close']
            profit = balance - (position * entry_price)
            trades.append({'type': 'sell', 'price': exit_price, 'time': row['open_time'], 'profit': profit})
            position = 0

    final_balance = balance if position == 0 else position * df.iloc[-1]['close']
    return trades, final_balance

def calculate_metrics(trades, initial_balance):
    profits = [t['profit'] for t in trades if t['type'] == 'sell']
    total_trades = len(profits)
    wins = [p for p in profits if p > 0]
    losses = [p for p in profits if p <= 0]

    win_rate = len(wins) / total_trades * 100 if total_trades > 0 else 0
    avg_profit = np.mean(profits) if profits else 0
    max_drawdown = min(profits) if losses else 0
    sharpe_ratio = (np.mean(profits) / np.std(profits)) if np.std(profits) != 0 else 0

    return {
        'Total Trades': total_trades,
        'Win Rate (%)': round(win_rate, 2),
        'Average Profit': round(avg_profit, 2),
        'Max Drawdown': round(max_drawdown, 2),
        'Sharpe Ratio': round(sharpe_ratio, 2)
    }
