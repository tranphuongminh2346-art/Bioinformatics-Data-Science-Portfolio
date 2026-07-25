"""
Stock Price Forecaster CLI Entrypoint
Author: Portfolio Creator
Description: CLI driver to load time series data, execute autoregressive feature engineering,
             fit a Ridge model, evaluate prediction errors, and output out-of-sample forecasts.
Language: English (100%)
"""

import argparse
import sys
import os

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from forecaster import StockPriceForecaster

def main():
    parser = argparse.ArgumentParser(
        description="Stock Price Forecaster - Train an autoregressive model and predict future prices."
    )
    parser.add_argument(
        "-i", "--input",
        default="stock_history.csv",
        help="Path to stock history CSV file (default: stock_history.csv)."
    )
    parser.add_argument(
        "-o", "--output",
        default="stock_forecast.png",
        help="Path to save forecast plot image (default: stock_forecast.png)."
    )
    parser.add_argument(
        "-s", "--steps",
        type=int,
        default=5,
        help="Number of days to forecast into the future (default: 5)."
    )

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"[-] Error: Input file '{args.input}' not found.", file=sys.stderr)
        sys.exit(1)

    print("=" * 60)
    print("Initializing Stock Price Time Series Forecaster")
    print("=" * 60)

    try:
        forecaster = StockPriceForecaster(args.input)
        clean_df = forecaster.engineer_features()
        print(f"[+] Loaded timeseries data.")
        print(f"    Raw records count: {len(forecaster.df)}")
        print(f"    Cleaned records count (after lag drops): {len(clean_df)}")
        print(f"    Autoregressive Features: {', '.join(forecaster.features)}")
    except Exception as e:
        print(f"[-] Feature engineering failed: {e}", file=sys.stderr)
        sys.exit(1)

    # 1. Sequential train-test split
    X_train, X_test, y_train, y_test, train_df, test_df = forecaster.train_test_split_sequential(clean_df)
    print(f"[*] Sequentially partitioned dataset:")
    print(f"    Training window days: {len(train_df)}")
    print(f"    Testing window days: {len(test_df)}")

    # 2. Train
    print("[*] Training autoregressive Ridge model...")
    try:
        forecaster.train(X_train, y_train)
        print("[+] Model training successful.")
    except Exception as e:
        print(f"[-] Model training failed: {e}", file=sys.stderr)
        sys.exit(1)

    # 3. Evaluate
    print("[*] Evaluating validation predictions on test partition...")
    try:
        metrics = forecaster.evaluate(X_test, y_test)
        mae = metrics["mae"]
        rmse = metrics["rmse"]
        print("\n" + "=" * 60)
        print("Model Performance Testing Scores")
        print("=" * 60)
        print(f"Mean Absolute Error (MAE): ${mae:.2f}")
        print(f"Root Mean Squared Error (RMSE): ${rmse:.2f}")
    except Exception as e:
        print(f"[-] Evaluation failed: {e}", file=sys.stderr)
        sys.exit(1)

    # 4. Out-of-sample recursive forecast
    print("\n" + "=" * 60)
    print(f"Recursive Out-of-Sample {args.steps}-Day Price Forecast")
    print("=" * 60)
    try:
        last_observation = clean_df.iloc[-1]
        future_preds = forecaster.forecast_multistep(last_observation, steps=args.steps)
        
        last_date = test_df['date'].iloc[-1]
        print(f"Forecast starting from last test date: {last_date.strftime('%Y-%m-%d')} (Price: ${last_observation['close_price']:.2f})")
        print("-" * 50)
        for day, price in enumerate(future_preds, 1):
            print(f"  Day t+{day}: Predicted Close Price = ${price:.2f}")
    except Exception as e:
        print(f"[-] Multistep forecast failed: {e}", file=sys.stderr)
        sys.exit(1)

    # 5. Plot
    print("\n" + "=" * 60)
    print("Generating Time Series Forecast Plot")
    print("=" * 60)
    try:
        print(f"[*] Saving forecast chart to: {args.output}")
        forecaster.plot_forecast(train_df, test_df, metrics['predictions'], future_preds, args.output)
        print("[+] Plot generation complete.")
    except Exception as e:
        print(f"[-] Plotting failed: {e}", file=sys.stderr)

    print("\nExecution complete.")

if __name__ == "__main__":
    main()
