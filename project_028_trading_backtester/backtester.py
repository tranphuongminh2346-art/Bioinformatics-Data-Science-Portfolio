"""
Stock Trading Strategy Backtester
Author: Portfolio Creator
Description: Backtests SMA crossover trading strategies, computes total returns,
             Sharpe ratios, and max drawdowns, and plots portfolio equity curves.
Language: English (100%)
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class TradingBacktester:
    """Simulates cash allocation ledger performance for moving average crossover strategies."""
    
    def __init__(self, data_path: str, initial_capital: float = 10000.0):
        self.data_path = data_path
        self.initial_capital = initial_capital
        self.df = None
        self.load_data()

    def load_data(self):
        """Loads historical close prices CSV database."""
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Stock prices file not found: {self.data_path}")
        self.df = pd.read_csv(self.data_path)
        self.df['date'] = pd.to_datetime(self.df['date'])
        self.df = self.df.sort_values('date').reset_index(drop=True)

    def run_backtest(self, short_window: int = 3, long_window: int = 5) -> dict:
        """
        Runs the SMA crossover trading simulation.
        
        Buy Signal: SMA_short > SMA_long
        Sell/Hold Signal: SMA_short <= SMA_long
        
        Returns:
            dict: Backtest metrics (total return, Sharpe ratio, max drawdown, ledger details).
        """
        # Calculate moving averages
        self.df['sma_short'] = self.df['close_price'].rolling(window=short_window).mean()
        self.df['sma_long'] = self.df['close_price'].rolling(window=long_window).mean()
        
        # Determine signals
        # 1 = Long position (Buy/Hold), 0 = Neutral position (Sell/Cash)
        self.df['signal'] = 0
        self.df.loc[self.df['sma_short'] > self.df['sma_long'], 'signal'] = 1
        
        # Position is shifted by 1 day because signal at day t takes effect at day t+1
        self.df['position'] = self.df['signal'].shift(1).fillna(0)
        
        # Calculate daily stock returns
        self.df['stock_return'] = self.df['close_price'].pct_change().fillna(0.0)
        
        # Calculate strategy daily returns
        self.df['strategy_return'] = self.df['position'] * self.df['stock_return']
        
        # Calculate cumulative returns and portfolio equity curve
        self.df['portfolio_value'] = self.initial_capital * (1.0 + self.df['strategy_return']).cumprod()
        
        # 1. Total Return
        final_value = self.df['portfolio_value'].iloc[-1]
        total_return = (final_value - self.initial_capital) / self.initial_capital
        
        # 2. Sharpe Ratio (assuming risk-free rate = 0, annualized assuming 252 trading days)
        strat_returns = self.df['strategy_return'].values[1:]  # exclude first day
        avg_ret = np.mean(strat_returns)
        std_ret = np.std(strat_returns)
        
        if std_ret == 0:
            sharpe_ratio = 0.0
        else:
            # Annualized Sharpe ratio
            sharpe_ratio = np.sqrt(252) * (avg_ret / std_ret)
            
        # 3. Maximum Drawdown
        roll_max = self.df['portfolio_value'].cummax()
        drawdown = (self.df['portfolio_value'] - roll_max) / roll_max
        max_drawdown = drawdown.min()
        
        return {
            "final_value": final_value,
            "total_return": total_return,
            "sharpe_ratio": sharpe_ratio,
            "max_drawdown": max_drawdown
        }

    def plot_backtest(self, output_path: str):
        """Plots stock prices + crossover indicators and portfolio value logs."""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 8), sharex=True)
        
        # 1. Price and SMA crossovers
        ax1.plot(self.df['date'], self.df['close_price'], color='#475569', lw=1.5, label='Close Price')
        ax1.plot(self.df['date'], self.df['sma_short'], color='#0284c7', linestyle='--', label='SMA Short')
        ax1.plot(self.df['date'], self.df['sma_long'], color='#10b981', linestyle='--', label='SMA Long')
        
        # Plot buy/sell signals
        # Buy signal marker: position changes from 0 to 1
        # Sell signal marker: position changes from 1 to 0
        self.df['trade_trigger'] = self.df['position'].diff().fillna(0)
        buys = self.df[self.df['trade_trigger'] == 1]
        sells = self.df[self.df['trade_trigger'] == -1]
        
        ax1.scatter(buys['date'], buys['close_price'], color='#10b981', marker='^', s=100, zorder=5, label='BUY Trigger')
        ax1.scatter(sells['date'], sells['close_price'], color='#ef4444', marker='v', s=100, zorder=5, label='SELL Trigger')
        
        ax1.set_title("Stock Price & Moving Average Crossover Indicators", fontsize=11, fontweight='bold')
        ax1.set_ylabel("Price ($)")
        ax1.grid(True, linestyle=':', alpha=0.5)
        ax1.legend(loc='upper left')
        
        # 2. Portfolio Equity Curve
        ax2.plot(self.df['date'], self.df['portfolio_value'], color='#f59e0b', lw=2, label='Equity Portfolio Value')
        ax2.axhline(self.initial_capital, color='#ef4444', linestyle=':', label='Initial Principal')
        ax2.set_title("Portfolio Equity Growth Ledger Curve", fontsize=11, fontweight='bold')
        ax2.set_xlabel("Date")
        ax2.set_ylabel("Equity ($)")
        ax2.grid(True, linestyle=':', alpha=0.5)
        ax2.legend(loc='upper left')
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150)
        plt.close()
