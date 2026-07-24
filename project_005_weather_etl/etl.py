"""
Weather ETL Pipeline Module
Author: Portfolio Creator
Description: Extracts weather data from Open-Meteo API (or cache),
             transforms values (Fahrenheit conversion, rolling averages),
             and creates visual analytics plots.
Language: English (100%)
"""

import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import requests

API_URL = "https://api.open-meteo.com/v1/forecast"

class WeatherETL:
    """ETL engine for handling temperature data from Open-Meteo."""
    
    def __init__(self, cache_path: str = "weather_cache.json"):
        self.cache_path = cache_path

    def extract(self, lat: float = None, lon: float = None) -> dict:
        """
        Extracts hourly weather data. Fetches from Open-Meteo API if coords are given,
        otherwise falls back to local cached weather json.
        
        Args:
            lat (float): Latitude.
            lon (float): Longitude.
            
        Returns:
            dict: Raw JSON response dict.
        """
        if lat is not None and lon is not None:
            print(f"[*] Querying live weather API for coordinates ({lat}, {lon})...")
            params = {
                "latitude": lat,
                "longitude": lon,
                "hourly": "temperature_2m",
                "timezone": "auto"
            }
            try:
                response = requests.get(API_URL, params=params, timeout=10)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                print(f"[-] API query failed: {e}. Falling back to cache.")
                
        # Cache fallback
        if os.path.exists(self.cache_path):
            print(f"[+] Loading cached weather data from: {self.cache_path}")
            with open(self.cache_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            raise FileNotFoundError(f"Cache file '{self.cache_path}' not found and no coordinates provided.")

    def transform(self, raw_data: dict) -> pd.DataFrame:
        """
        Transforms the raw JSON weather payload:
        - Extracts time and temp_2m arrays.
        - Calculates Fahrenheit conversion.
        - Calculates 3-hour rolling temperature average.
        
        Args:
            raw_data (dict): Raw API/Cache dict.
            
        Returns:
            pd.DataFrame: Transformed records.
        """
        hourly = raw_data.get("hourly", {})
        times = hourly.get("time", [])
        temps_c = hourly.get("temperature_2m", [])
        
        if not times or not temps_c:
            raise ValueError("Parsed weather payload does not contain hourly time or temperature arrays.")
            
        df = pd.DataFrame({
            "timestamp": times,
            "temperature_c": temps_c
        })
        
        # 1. Celsius to Fahrenheit
        df["temperature_f"] = df["temperature_c"] * 1.8 + 32.0
        
        # 2. Rolling average (3-hour window, min_periods=1 to avoid NaNs at start)
        df["rolling_avg_c"] = df["temperature_c"].rolling(window=3, min_periods=1).mean()
        
        # Round values for clean database presentation
        df = df.round(2)
        return df

    def generate_plot(self, df: pd.DataFrame, output_path: str):
        """
        Generates and saves a premium line chart of temperatures and rolling averages.
        
        Args:
            df (pd.DataFrame): Transformed weather dataframe.
            output_path (str): File path to save plot.
        """
        plt.figure(figsize=(10, 5))
        
        # Parse timestamp strings for cleaner x-axis labels
        hours = [t.split("T")[-1] for t in df["timestamp"]]
        
        plt.plot(hours, df["temperature_c"], color='#0284c7', marker='o', linewidth=2, label="Actual Temp (°C)")
        plt.plot(hours, df["rolling_avg_c"], color='#f97316', linestyle='--', linewidth=1.5, label="3-Hour Rolling Avg (°C)")
        
        # Visual enhancements
        plt.title("Hourly Temperature Profile & Rolling Trend", fontsize=12, fontweight='bold', pad=15)
        plt.xlabel("Time of Day", fontsize=10)
        plt.ylabel("Temperature (°C)", fontsize=10)
        plt.grid(True, linestyle=':', alpha=0.6)
        plt.xticks(rotation=45, fontsize=8)
        plt.legend(loc="upper right")
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150)
        plt.close()
