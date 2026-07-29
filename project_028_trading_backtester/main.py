"""
Stock Backtester CLI
Author: Portfolio Creator
Description: CLI driver to execute moving average crossovers backtesting.
Language: English (100%)
"""

import argparse
import sys
import os

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backtester import TradingBacktester

def main():
    parser = argparse.ArgumentParser(
        description="Stock Trading Strategy Backtester - SMA crossover backtester."
    )
    parser.add_argument(
        "-i", "--input",
        default="stock_prices.csv",
        help="Path to input stock prices CSV (default: stock_prices.csv)."
    )
    parser.add_argument(
        "-o", "--output",
        default="backtest_result.png",
        help="Path to save output chart (default: backtest_result.png)."
    )
    parser.add_argument(
        "-s", "--short",
        type=int,
        default=3,
        help="Short SMA window size in days (default: 3)."
    )
    parser.add_argument(
        "-l", "--long",
        type=int,
        default=5,
        help="Long SMA window size in days (default: 5)."
    )
    parser.add_argument(
        "-c", "--capital",
        type=float,
        default=10000.0,
        help="Initial capital balance in USD (default: 10000.0)."
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Stock Moving Average Crossover Backtester Pipeline")
    print("=" * 60)
    print(f"[*] Input Data:      {args.input}")
    print(f"[*] Initial Principal: ${args.capital:,.2f}")
    print(f"[*] Short window:    {args.short} days | Long window: {args.long} days")
    print(f"[*] Saving plot to:  {args.output}")

    try:
        backtester = TradingBacktester(args.input, initial_capital=args.capital)
        print(f"[+] Loaded {len(backtester.df)} historical close prices.")
        
        # Run Backtest
        print("[*] Simulating transactions ledger and performance metrics...")
        metrics = backtester.run_backtest(short_window=args.short, long_window=args.long)
        
        # Print results
        print("\n" + "=" * 60)
        print("Backtest Simulation Metrics Results")
        print("=" * 60)
        print(f"[*] Final Portfolio Value : ${metrics['final_value']:,.2f}")
        print(f"[*] Cumulative Return     : {metrics['total_return'] * 100:.2f}%")
        print(f"[*] Sharpe Ratio (Ann.)   : {metrics['sharpe_ratio']:.4f}")
        print(f"[*] Maximum Drawdown      : {metrics['max_drawdown'] * 100:.2f}%")
        
        # Save plots
        print("\n[*] Saving crossover markers and equity curve plot...")
        backtester.plot_backtest(args.output)
        print(f"[+] Output chart saved successfully.")
        
    except Exception as e:
        print(f"[-] Pipeline execution failed: {e}", file=sys.stderr)
        sys.exit(1)

    print("\nExecution complete.")

if __name__ == "__main__":
    main()
