"""
Acid-Base pH Titration Curve Simulator
Author: Portfolio Creator
Description: Simulates the pH curve of weak acid / strong base titration,
             solves equilibrium equations, and exports curves graphs.
Language: English (100%)
"""

import numpy as np
import matplotlib.pyplot as plt

class PHTitrator:
    """Simulates chemical pH levels during acid-base titration processes."""
    
    def __init__(self, c_acid: float = 0.1, v_acid: float = 50.0, pka: float = 4.76, c_base: float = 0.1):
        self.c_acid = c_acid        # Molarity of weak acid (M)
        self.v_acid = v_acid        # Volume of weak acid (mL)
        self.pka = pka              # Acid dissociation constant exponent
        self.ka = 10 ** (-pka)
        self.c_base = c_base        # Molarity of strong base (M)
        
        # Kw water self-ionization constant
        self.kw = 1e-14
        
        # Equivalence Volume V_eq: C_a * V_a = C_b * V_eq -> V_eq = (C_a * V_a) / C_b
        self.v_eq = (self.c_acid * self.v_acid) / self.c_base

    def calculate_ph_at_volume(self, v_added: float) -> float:
        """
        Solves chemical equilibrium equations to calculate pH for a volume of added strong base.
        
        Returns:
            float: Calculated pH value.
        """
        if v_added < 0:
            raise ValueError("Base volume cannot be negative.")
            
        # 1. Before Titration Starts
        if v_added == 0:
            # Weak acid ionization: [H+] = sqrt(Ka * Ca)
            # Using log version: pH = 0.5 * (pKa - log10(Ca))
            h_conc = np.sqrt(self.ka * self.c_acid)
            return -np.log10(h_conc)
            
        # 2. Before Equivalence Point (Buffer Region)
        elif v_added < self.v_eq:
            # Henderson-Hasselbalch equation: pH = pKa + log10([A-] / [HA])
            # Moles added base (A-) = C_b * V_b
            # Moles remaining acid (HA) = C_a * V_a - C_b * V_b
            moles_a = self.c_base * v_added
            moles_ha = (self.c_acid * self.v_acid) - (self.c_base * v_added)
            
            ratio = moles_a / moles_ha
            return self.pka + np.log10(ratio)
            
        # 3. At Equivalence Point
        elif np.isclose(v_added, self.v_eq, atol=1e-5):
            # Pure weak base salt: A- + H2O <-> HA + OH-
            # Kb = Kw / Ka
            # [OH-] = sqrt(Kb * C_salt)
            kb = self.kw / self.ka
            total_vol = self.v_acid + self.v_eq
            c_salt = (self.c_acid * self.v_acid) / total_vol
            
            oh_conc = np.sqrt(kb * c_salt)
            poh = -np.log10(oh_conc)
            return 14.0 - poh
            
        # 4. After Equivalence Point (Excess Strong Base)
        else:
            # Excess base moles = C_b * (V_b - V_eq)
            # Total volume = V_a + V_b
            excess_moles = self.c_base * (v_added - self.v_eq)
            total_vol = self.v_acid + v_added
            oh_conc = excess_moles / total_vol
            
            poh = -np.log10(oh_conc)
            return 14.0 - poh

    def generate_curve(self, steps: int = 200) -> tuple:
        """
        Generates volume increments and calculates corresponding pH arrays.
        
        Returns:
            tuple: (volumes: np.ndarray, ph_values: np.ndarray)
        """
        # Volume added goes up to twice the equivalence point
        max_vol = self.v_eq * 2.0
        volumes = np.linspace(0.0, max_vol, steps)
        ph_values = np.array([self.calculate_ph_at_volume(v) for v in volumes])
        return volumes, ph_values

    def plot_titration(self, output_path: str):
        """Plots the titration curve and labels equivalence point."""
        volumes, ph_vals = self.generate_curve()
        
        plt.figure(figsize=(7, 6))
        plt.plot(volumes, ph_vals, color='#0284c7', lw=2, label='Titration Curve')
        
        # Draw Equivalence point indicator
        eq_ph = self.calculate_ph_at_volume(self.v_eq)
        plt.scatter(self.v_eq, eq_ph, color='#ef4444', s=100, zorder=5, label='Equivalence Point')
        plt.axvline(self.v_eq, color='#ef4444', linestyle=':')
        plt.axhline(eq_ph, color='#ef4444', linestyle=':')
        
        plt.title(f"Weak Acid / Strong Base pH Titration Curve\n(pKₐ = {self.pka})", fontsize=11, fontweight='bold')
        plt.xlabel("Volume of NaOH Added (mL)")
        plt.ylabel("pH")
        plt.ylim(0, 14)
        plt.grid(True, linestyle=':', alpha=0.5)
        plt.legend()
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150)
        plt.close()
