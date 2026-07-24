"""
COVID-19 Time Series Analyzer
Author: Portfolio Creator
Description: Processes cumulative COVID-19 cases/deaths, calculates daily new cases,
             computes rolling averages, and plots trendlines.
Language: English (100%)
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

class CovidTimeSeriesAnalyzer:
    """Analyzes daily COVID-19 metrics from cumulative logs."""
    
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.df = None
        self.load_data()

    def load_data(self):
        """Loads and preprocesses the cumulative timeseries data."""
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"COVID dataset not found: {self.data_path}")
            
        self.df = pd.read_csv(self.data_path)
        self.df['date'] = pd.to_datetime(self.df['date'])
        self.df = self.df.sort_values('date').reset_index(drop=True)

    def calculate_daily_metrics(self) -> pd.DataFrame:
        """
        Calculates daily new cases, new deaths, rolling averages, and growth rates.
        
        Returns:
            pd.DataFrame: Transformed dataset.
        """
        # Calculate daily new entries (diff from cumulative)
        # Fill NaN at index 0 with cumulative value itself
        self.df['new_cases'] = self.df['confirmed_cases'].diff().fillna(self.df['confirmed_cases'].iloc[0])
        self.df['new_deaths'] = self.df['confirmed_deaths'].diff().fillna(self.df['confirmed_deaths'].iloc[0])
        
        # Ensure values are non-negative
        self.df['new_cases'] = self.df['new_cases'].clip(lower=0)
        self.df['new_deaths'] = self.df['new_deaths'].clip(lower=0)

        # 7-day rolling averages
        self.df['new_cases_rolling'] = self.df['new_cases'].rolling(window=7, min_periods=1).mean()
        self.df['new_deaths_rolling'] = self.df['new_deaths'].rolling(window=7, min_periods=1).mean()
        
        # Daily growth rate of new cases
        self.df['case_growth_rate'] = self.df['new_cases'].pct_change().fillna(0.0)
        
        return self.df

    def plot_dashboard(self, output_path: str):
        """
        Creates a dual y-axis dashboard trend plot.
        
        Args:
            output_path (str): File path to save plot.
        """
        if 'new_cases' not in self.df.columns:
            self.calculate_daily_metrics()
            
        fig, ax1 = plt.subplots(figsize=(10, 6))

        color = '#0284c7'
        ax1.set_xlabel('Date', fontsize=10)
        ax1.set_ylabel('Daily New Cases', color=color, fontsize=10)
        
        # Plot daily cases bar chart and rolling average line
        ax1.bar(self.df['date'], self.df['new_cases'], color=color, alpha=0.3, label="Daily New Cases")
        ax1.plot(self.df['date'], self.df['new_cases_rolling'], color='#0369a1', linewidth=2, label="7-Day Case Avg")
        ax1.tick_params(axis='y', labelcolor=color)
        
        # Instantiate a second axes sharing the x-axis
        ax2 = ax1.twinx()  
        color_death = '#ef4444'
        ax2.set_ylabel('Daily New Deaths', color=color_death, fontsize=10)
        
        # Plot daily deaths rolling average
        ax2.plot(self.df['date'], self.df['new_deaths_rolling'], color=color_death, linewidth=2, linestyle='--', label="7-Day Death Avg")
        ax2.tick_params(axis='y', labelcolor=color_death)

        # Align titles and layouts
        plt.title("COVID-19 Daily Trends & 7-Day Moving Averages", fontsize=12, fontweight='bold', pad=15)
        fig.tight_layout()
        
        # Combined legends
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

        plt.grid(True, linestyle=':', alpha=0.5)
        plt.savefig(output_path, dpi=150)
        plt.close()
