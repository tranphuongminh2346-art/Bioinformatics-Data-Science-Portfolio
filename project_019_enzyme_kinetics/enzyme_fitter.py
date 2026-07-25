"""
Enzyme Kinetics Fitter
Author: Portfolio Creator
Description: Fits substrate velocity data to the Michaelis-Menten equation,
             extracts Vmax and Km parameters, and performs double reciprocal transforms.
Language: English (100%)
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def michaelis_menten(s, vmax, km):
    """Michaelis-Menten kinetics equation."""
    return (vmax * s) / (km + s)

class EnzymeKineticsFitter:
    """Performs regression fitting on substrate concentrations and velocities."""
    
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.df = None
        self.vmax = None
        self.km = None
        self.pcov = None
        self.load_data()

    def load_data(self):
        """Loads kinetics data from CSV."""
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Kinetics data file not found: {self.data_path}")
        self.df = pd.read_csv(self.data_path)

    def fit_parameters(self) -> tuple:
        """
        Fits Michaelis-Menten parameter metrics using non-linear least squares.
        
        Returns:
            tuple: (Vmax, Km)
        """
        s = self.df['substrate_concentration'].values
        v = self.df['velocity'].values
        
        # Initial guess: Vmax is max velocity, Km is median substrate
        p0 = [np.max(v), np.median(s)]
        
        # Non-linear curve fitting
        popt, pcov = curve_fit(michaelis_menten, s, v, p0=p0, bounds=(0, np.inf))
        
        self.vmax = popt[0]
        self.km = popt[1]
        self.pcov = pcov
        
        return self.vmax, self.km

    def get_lineweaver_burk(self) -> pd.DataFrame:
        """
        Computes Lineweaver-Burk double reciprocal values.
        
        Returns:
            pd.DataFrame: DataFrame containing 1/S and 1/v.
        """
        lb_df = pd.DataFrame()
        lb_df['reciprocal_s'] = 1.0 / self.df['substrate_concentration']
        lb_df['reciprocal_v'] = 1.0 / self.df['velocity']
        return lb_df

    def plot_kinetics(self, output_path: str):
        """Generates MM and Lineweaver-Burk diagnostic plots."""
        if self.vmax is None or self.km is None:
            raise ValueError("Model parameters must be fit before plotting.")
            
        s = self.df['substrate_concentration'].values
        v = self.df['velocity'].values
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # 1. Michaelis-Menten Plot
        s_fit = np.linspace(0, np.max(s) * 1.1, 200)
        v_fit = michaelis_menten(s_fit, self.vmax, self.km)
        
        ax1.scatter(s, v, color='#0284c7', zorder=5, label='Experimental Data')
        ax1.plot(s_fit, v_fit, color='#ef4444', lw=2, label=f'MM Fit\n(Vmax={self.vmax:.2f}, Km={self.km:.2f})')
        ax1.axhline(self.vmax, color='#475569', linestyle='--', alpha=0.7, label='Vmax Asymptote')
        ax1.axvline(self.km, color='#10b981', linestyle=':', alpha=0.7, label='Km (1/2 Vmax)')
        
        ax1.set_title("Michaelis-Menten Enzyme Kinetics", fontsize=11, fontweight='bold')
        ax1.set_xlabel("Substrate Concentration [S] (mM)")
        ax1.set_ylabel("Reaction Velocity V (µmol/min)")
        ax1.grid(True, linestyle=':', alpha=0.6)
        ax1.legend(loc='lower right')
        
        # 2. Lineweaver-Burk Plot
        lb_df = self.get_lineweaver_burk()
        recip_s = lb_df['reciprocal_s'].values
        recip_v = lb_df['reciprocal_v'].values
        
        # Line fit based on parameters: 1/V = (Km/Vmax)*(1/S) + (1/Vmax)
        slope = self.km / self.vmax
        intercept = 1.0 / self.vmax
        
        recip_s_fit = np.linspace(-1.0 / self.km, np.max(recip_s) * 1.1, 200)
        recip_v_fit = slope * recip_s_fit + intercept
        
        ax2.scatter(recip_s, recip_v, color='#0284c7', zorder=5, label='Reciprocal Data')
        ax2.plot(recip_s_fit, recip_v_fit, color='#ef4444', lw=2, label='Double Reciprocal Line')
        
        # Intercept highlights
        ax2.axvline(0, color='#475569', lw=1)
        ax2.axhline(0, color='#475569', lw=1)
        ax2.scatter(-1.0 / self.km, 0, color='#10b981', s=50, zorder=6, label='x-intercept (-1/Km)')
        ax2.scatter(0, intercept, color='#f59e0b', s=50, zorder=6, label='y-intercept (1/Vmax)')
        
        ax2.set_title("Lineweaver-Burk Double Reciprocal Plot", fontsize=11, fontweight='bold')
        ax2.set_xlabel("1 / [S] (1/mM)")
        ax2.set_ylabel("1 / V (min/µmol)")
        ax2.grid(True, linestyle=':', alpha=0.6)
        ax2.legend(loc='upper left')
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150)
        plt.close()
