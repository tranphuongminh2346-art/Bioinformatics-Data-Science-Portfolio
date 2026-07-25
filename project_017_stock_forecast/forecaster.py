"""
Stock Time Series Forecaster with Lag Features
Author: Portfolio Creator
Description: Builds autoregressive features (lags, rolling stats), trains a Ridge
             regression model using time-based sequential splits, and plots forecasts.
Language: English (100%)
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error

class StockPriceForecaster:
    """Autoregressive Ridge regression model for stock close price forecasting."""
    
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.df = None
        self.features = []
        self.model = Ridge(alpha=1.0)
        self.is_trained = False
        self.load_data()

    def load_data(self):
        """Loads stock price timeseries."""
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Stock history CSV not found: {self.data_path}")
        self.df = pd.read_csv(self.data_path)
        self.df['date'] = pd.to_datetime(self.df['date'])
        self.df = self.df.sort_values('date').reset_index(drop=True)

    def engineer_features(self) -> pd.DataFrame:
        """
        Generates lag and rolling window features for autoregressive forecasting.
        - lag_1, lag_2, lag_3: Close price of previous days.
        - rolling_mean_3: 3-day moving average of close prices.
        - rolling_std_3: 3-day standard deviation (volatility).
        
        Returns:
            pd.DataFrame: Engineered feature dataset with NaNs dropped.
        """
        # Create lag variables
        self.df['lag_1'] = self.df['close_price'].shift(1)
        self.df['lag_2'] = self.df['close_price'].shift(2)
        self.df['lag_3'] = self.df['close_price'].shift(3)
        
        # Create rolling variables
        # Note: We must shift close_price by 1 first so rolling stats do not leak target close_price!
        self.df['rolling_mean_3'] = self.df['close_price'].shift(1).rolling(window=3).mean()
        self.df['rolling_std_3'] = self.df['close_price'].shift(1).rolling(window=3).std()
        
        self.features = ['lag_1', 'lag_2', 'lag_3', 'rolling_mean_3', 'rolling_std_3']
        
        # Drop rows with NaN (first 3 rows due to lag 3 and window 3)
        clean_df = self.df.dropna().reset_index(drop=True)
        return clean_df

    def train_test_split_sequential(self, clean_df: pd.DataFrame, train_ratio: float = 0.8) -> tuple:
        """
        Splits data sequentially by time (no random shuffling to prevent leakage).
        
        Returns:
            tuple: (X_train, X_test, y_train, y_test, train_df, test_df)
        """
        n = len(clean_df)
        split_idx = int(n * train_ratio)
        
        train_df = clean_df.iloc[:split_idx]
        test_df = clean_df.iloc[split_idx:]
        
        X_train = train_df[self.features]
        y_train = train_df['close_price']
        
        X_test = test_df[self.features]
        y_test = test_df['close_price']
        
        return X_train, X_test, y_train, y_test, train_df, test_df

    def train(self, X_train, y_train):
        """Fits the regression model."""
        self.model.fit(X_train, y_train)
        self.is_trained = True

    def evaluate(self, X_test, y_test) -> dict:
        """
        Evaluates the forecaster on a test set.
        
        Returns:
            dict: Performance metrics.
        """
        if not self.is_trained:
            raise ValueError("Model must be trained.")
        y_pred = self.model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        return {
            "mae": mae,
            "rmse": rmse,
            "predictions": y_pred
        }

    def forecast_multistep(self, last_row: pd.Series, steps: int = 5) -> list:
        """
        Performs recursive multi-step out-of-sample forecasting.
        Calculates feature inputs for day t+1 dynamically from day t predictions.
        
        Returns:
            list: List of forecasted prices.
        """
        if not self.is_trained:
            raise ValueError("Model must be trained.")
            
        forecasts = []
        
        # Initialize history queue using the most recent 3 close prices
        # last_row contains: close_price, lag_1, lag_2, lag_3, rolling_mean_3, rolling_std_3
        p_t = last_row['close_price']
        p_t_minus_1 = last_row['lag_1']
        p_t_minus_2 = last_row['lag_2']
        
        history = [p_t_minus_2, p_t_minus_1, p_t]
        
        for _ in range(steps):
            # Features for next step:
            # lag_1 = history[-1]
            # lag_2 = history[-2]
            # lag_3 = history[-3]
            l1, l2, l3 = history[-1], history[-2], history[-3]
            
            # rolling stats
            r_mean = np.mean(history[-3:])
            r_std = np.std(history[-3:]) if len(history) >= 3 else 0.0
            
            input_features = np.array([l1, l2, l3, r_mean, r_std]).reshape(1, -1)
            input_df = pd.DataFrame(input_features, columns=self.features)
            pred = float(self.model.predict(input_df)[0])
            
            forecasts.append(pred)
            # Append predicted price to history to feed next step features
            history.append(pred)
            
        return forecasts

    def plot_forecast(self, train_df, test_df, y_pred_test, future_forecasts, output_path: str):
        """
        Plots historic close values, test fits, and future forecasting predictions.
        
        Args:
            output_path (str): Save path for chart.
        """
        plt.figure(figsize=(10, 6))
        
        # Combine training and testing dates
        plt.plot(train_df['date'], train_df['close_price'], color='#475569', label='Train History')
        plt.plot(test_df['date'], test_df['close_price'], color='#0284c7', marker='o', label='Test Actual')
        plt.plot(test_df['date'], y_pred_test, color='#f97316', linestyle='--', marker='x', label='Test Predicted')
        
        # Plot future forecast
        # Generate future dates
        last_date = test_df['date'].iloc[-1]
        future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=len(future_forecasts), freq='B')
        
        plt.plot(future_dates, future_forecasts, color='#ef4444', marker='s', linestyle=':', label='Future Forecast')
        
        plt.title('Stock Close Price Forecasting (Autoregressive Ridge Fit)', fontsize=12, fontweight='bold', pad=15)
        plt.xlabel('Date', fontsize=10)
        plt.ylabel('Close Price ($)', fontsize=10)
        plt.grid(True, linestyle=':', alpha=0.5)
        plt.legend(loc='upper left')
        plt.xticks(rotation=45, fontsize=8)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150)
        plt.close()
