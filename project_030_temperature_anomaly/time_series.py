"""
Climate Temperature Anomaly Time Series Analyzer
Author: Portfolio Creator
Description: Decomposes temperature anomaly timeseries logs into trend, seasonal, and residuals,
             estimates global warming slopes, and generates diagnostic plots.
Language: English (100%)
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose

class TemperatureAnomalyAnalyzer:
    """Analyzes climatological temperature timeseries records using seasonal decomposition."""
    
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.df = None
        self.decomposition = None
        self.slope = None
        self.intercept = None
        self.load_data()

    def load_data(self):
        """Loads anomaly logs and sets DatetimeIndex."""
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Temperature data not found: {self.data_path}")
        self.df = pd.read_csv(self.data_path)
        self.df['date'] = pd.to_datetime(self.df['date'])
        self.df = self.df.sort_values('date').set_index('date')

    def decompose_series(self, period: int = 12) -> tuple:
        """
        Performs additive seasonal decomposition.
        
        Returns:
            tuple: (trend: pd.Series, seasonal: pd.Series, resid: pd.Series)
        """
        if len(self.df) < period * 2:
            raise ValueError(f"Dataset must have at least {period * 2} entries for period {period} decomposition.")
            
        self.decomposition = seasonal_decompose(self.df['anomaly'], model='additive', period=period)
        return (
            self.decomposition.trend,
            self.decomposition.seasonal,
            self.decomposition.resid
        )

    def calculate_trend_slope(self) -> float:
        """
        Fits a linear regression model to compute anomaly trend slope.
        
        Returns:
            float: Slope in degrees Celsius per year.
        """
        # Represent time as index number (0, 1, 2, ...)
        x = np.arange(len(self.df))
        y = self.df['anomaly'].values
        
        # Fit linear polynomial y = ax + b
        slope, intercept = np.polyfit(x, y, 1)
        self.slope = slope
        self.intercept = intercept
        
        return self.slope

    def plot_analysis(self, output_path: str):
        """Generates 4-panel timeseries decomposition diagnostic charts."""
        if self.decomposition is None:
            self.decompose_series()
            
        fig, axes = plt.subplots(4, 1, figsize=(11, 10), sharex=True)
        
        # 1. Observed
        axes[0].plot(self.df.index, self.df['anomaly'], color='#475569', label='Observed Anomaly')
        if self.slope is not None:
            # Plot trendline
            x_vals = np.arange(len(self.df))
            trendline = self.slope * x_vals + self.intercept
            axes[0].plot(self.df.index, trendline, color='#ef4444', linestyle='--', label='Linear Trend')
            
        axes[0].set_ylabel("Anomaly (°C)")
        axes[0].set_title("Global Temperature Anomaly Seasonal Decomposition", fontsize=12, fontweight='bold')
        axes[0].grid(True, linestyle=':', alpha=0.5)
        axes[0].legend(loc='upper left')
        
        # 2. Trend
        axes[1].plot(self.df.index, self.decomposition.trend, color='#0284c7', label='Decomposed Trend')
        axes[1].set_ylabel("Trend (°C)")
        axes[1].grid(True, linestyle=':', alpha=0.5)
        axes[1].legend(loc='upper left')
        
        # 3. Seasonal
        axes[2].plot(self.df.index, self.decomposition.seasonal, color='#10b981', label='Seasonal Cycle')
        axes[2].set_ylabel("Seasonal (°C)")
        axes[2].grid(True, linestyle=':', alpha=0.5)
        axes[2].legend(loc='upper left')
        
        # 4. Residuals
        axes[3].scatter(self.df.index, self.decomposition.resid, color='#f59e0b', s=20, label='Residuals')
        axes[3].axhline(0, color='#475569', linestyle=':')
        axes[3].set_ylabel("Residual (°C)")
        axes[3].set_xlabel("Date")
        axes[3].grid(True, linestyle=':', alpha=0.5)
        axes[3].legend(loc='upper left')
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150)
        plt.close()
