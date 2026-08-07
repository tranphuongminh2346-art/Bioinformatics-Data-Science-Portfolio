"""
ECG Heart Rate Variability (HRV) Extractor
Author: Portfolio Creator
Description: Computes time-domain (SDNN, RMSSD, pNN50) and frequency-domain
             (LF, HF, LF/HF) metrics from heartbeat R-R interval timeseries.
Language: English (100%)
"""

import os
import pandas as pd
import numpy as np

class HRVExtractor:
    """Extracts autonomic nervous system parameters from R-R interval timeseries."""
    
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.rr_intervals = None
        self.load_data()

    def load_data(self):
        """Loads R-R intervals list from CSV (values in milliseconds)."""
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"RR intervals file not found: {self.data_path}")
        df = pd.read_csv(self.data_path)
        self.rr_intervals = df['rr_interval'].values

    def calculate_time_domain(self) -> dict:
        """
        Calculates time-domain HRV statistics.
        
        Returns:
            dict: Mean RR, Mean HR, SDNN, RMSSD, pNN50.
        """
        rr = self.rr_intervals
        n = len(rr)
        if n < 2:
            raise ValueError("At least 2 intervals required to calculate HRV metrics.")
            
        mean_rr = np.mean(rr)
        # HR (bpm) = 60000 / Mean RR (ms)
        mean_hr = 60000.0 / mean_rr
        
        # SDNN: Standard deviation of normal-to-normal intervals
        sdnn = np.std(rr, ddof=1)
        
        # RMSSD: Root mean square of successive differences
        diffs = np.diff(rr)
        rmssd = np.sqrt(np.mean(diffs ** 2))
        
        # pNN50: percentage of differences > 50 ms
        nn50 = np.sum(np.abs(diffs) > 50.0)
        pnn50 = (nn50 / len(diffs)) * 100.0
        
        return {
            "mean_rr": mean_rr,
            "mean_hr": mean_hr,
            "sdnn": sdnn,
            "rmssd": rmssd,
            "pnn50": pnn50
        }

    def calculate_frequency_domain(self, fs: float = 4.0) -> dict:
        """
        Interpolates irregular RR timeseries and computes spectral powers.
        
        LF Band: 0.04 - 0.15 Hz (sympathetic & parasympathetic activity)
        HF Band: 0.15 - 0.40 Hz (vagal/parasympathetic activity)
        
        Returns:
            dict: LF power, HF power, LF/HF ratio.
        """
        rr = self.rr_intervals
        
        # Convert cumulative RR intervals to timestamps in seconds
        timestamps = np.cumsum(rr) / 1000.0
        t_start = timestamps[0]
        t_end = timestamps[-1]
        
        # Resample on regular grid (e.g. at 4 Hz)
        t_grid = np.arange(t_start, t_end, 1.0 / fs)
        if len(t_grid) < 8:
            return {"lf_power": 0.0, "hf_power": 0.0, "lf_hf_ratio": 0.0}
            
        # Linear interpolation
        rr_interpolated = np.interp(t_grid, timestamps, rr)
        
        # Detrend signals to remove 0 Hz component
        rr_detrended = rr_interpolated - np.mean(rr_interpolated)
        
        # Compute FFT
        n_samples = len(t_grid)
        fft_vals = np.fft.rfft(rr_detrended)
        freqs = np.fft.rfftfreq(n_samples, d=1.0/fs)
        
        # Power Spectral Density (PSD)
        psd = (np.abs(fft_vals) ** 2) / n_samples
        
        # Extract band powers
        lf_mask = (freqs >= 0.04) & (freqs <= 0.15)
        hf_mask = (freqs >= 0.15) & (freqs <= 0.40)
        
        lf_power = np.sum(psd[lf_mask])
        hf_power = np.sum(psd[hf_mask])
        
        # Protect against division by zero
        if hf_power == 0:
            ratio = 0.0
        else:
            ratio = lf_power / hf_power
            
        return {
            "lf_power": lf_power,
            "hf_power": hf_power,
            "lf_hf_ratio": ratio
        }
