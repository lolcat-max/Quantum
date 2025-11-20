import tkinter as tk
from tkinter import ttk, scrolledtext
import random
import threading
import time

class NuclearSSPSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("SSP Nuclear Physics Simulator")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1a1a2e')
        
        self.numbers = []
        self.target = 0
        self.solution = None
        self.running = False
        self.generated_subset = []
        
        # Atomic data with production energies and nuclear shell model
        # BE = Total Binding Energy, SEP = Separation Energy for last nucleon
        # Production = Energy required to assemble from free nucleons
        self.atomic_data = {
            'Hydrogen (H-1)': {
                'Z': 1, 'N': 0, 'BE': 0, 'BE_per_A': 0, 'SEP_n': 0, 'SEP_p': 0,
                'shells': [1], 'magic': False, 'stability': 'stable',
                'production_MeV': 0, 'formation': 'primordial'
            },
            'Helium (He-4)': {
                'Z': 2, 'N': 2, 'BE': 28.296, 'BE_per_A': 7.074, 'SEP_n': 20.58, 'SEP_p': 19.81,
                'shells': [2], 'magic': True, 'stability': 'stable',
                'production_MeV': 28.296, 'formation': 'Big Bang nucleosynthesis'
            },
            'Carbon (C-12)': {
                'Z': 6, 'N': 6, 'BE': 92.162, 'BE_per_A': 7.680, 'SEP_n': 18.72, 'SEP_p': 15.96,
                'shells': [2, 4, 6], 'magic': False, 'stability': 'stable',
                'production_MeV': 92.162, 'formation': 'Triple-alpha process in stars'
            },
            'Nitrogen (N-14)': {
                'Z': 7, 'N': 7, 'BE': 104.659, 'BE_per_A': 7.476, 'SEP_n': 10.55, 'SEP_p': 7.55,
                'shells': [2, 5, 7], 'magic': False, 'stability': 'stable',
                'production_MeV': 104.659, 'formation': 'CNO cycle in stars'
            },
            'Oxygen (O-16)': {
                'Z': 8, 'N': 8, 'BE': 127.619, 'BE_per_A': 7.976, 'SEP_n': 15.66, 'SEP_p': 12.13,
                'shells': [2, 6, 8], 'magic': True, 'stability': 'stable',
                'production_MeV': 127.619, 'formation': 'Helium burning in massive stars'
            },
            'Sodium (Na-23)': {
                'Z': 11, 'N': 12, 'BE': 186.564, 'BE_per_A': 8.112, 'SEP_n': 12.42, 'SEP_p': 8.79,
                'shells': [2, 8, 11, 2], 'magic': False, 'stability': 'stable',
                'production_MeV': 186.564, 'formation': 'Carbon burning'
            },
            'Magnesium (Mg-24)': {
                'Z': 12, 'N': 12, 'BE': 198.257, 'BE_per_A': 8.261, 'SEP_n': 16.53, 'SEP_p': 11.69,
                'shells': [2, 8, 12], 'magic': False, 'stability': 'stable',
                'production_MeV': 198.257, 'formation': 'Carbon/Neon burning'
            },
            'Aluminum (Al-27)': {
                'Z': 13, 'N': 14, 'BE': 224.952, 'BE_per_A': 8.332, 'SEP_n': 13.06, 'SEP_p': 8.27,
                'shells': [2, 8, 13, 4], 'magic': False, 'stability': 'stable',
                'production_MeV': 224.952, 'formation': 'Neon burning'
            },
            'Silicon (Si-28)': {
                'Z': 14, 'N': 14, 'BE': 236.537, 'BE_per_A': 8.448, 'SEP_n': 17.18, 'SEP_p': 11.58,
                'shells': [2, 8, 14], 'magic': True, 'stability': 'stable',
                'production_MeV': 236.537, 'formation': 'Oxygen burning'
            },
            'Phosphorus (P-31)': {
                'Z': 15, 'N': 16, 'BE': 262.917, 'BE_per_A': 8.481, 'SEP_n': 12.31, 'SEP_p': 7.30,
                'shells': [2, 8, 15, 6], 'magic': False, 'stability': 'stable',
                'production_MeV': 262.917, 'formation': 'Silicon burning'
            },
            'Sulfur (S-32)': {
                'Z': 16, 'N': 16, 'BE': 271.782, 'BE_per_A': 8.493, 'SEP_n': 15.04, 'SEP_p': 8.86,
                'shells': [2, 8, 16], 'magic': False, 'stability': 'stable',
                'production_MeV': 271.782, 'formation': 'Silicon burning'
            },
            'Chlorine (Cl-35)': {
                'Z': 17, 'N': 18, 'BE': 298.208, 'BE_per_A': 8.520, 'SEP_n': 12.64, 'SEP_p': 6.48,
                'shells': [2, 8, 17, 8], 'magic': False, 'stability': 'stable',
                'production_MeV': 298.208, 'formation': 'Silicon burning'
            },
            'Argon (Ar-40)': {
                'Z': 18, 'N': 22, 'BE': 343.810, 'BE_per_A': 8.595, 'SEP_n': 15.24, 'SEP_p': 7.04,
                'shells': [2, 8, 18, 12], 'magic': False, 'stability': 'stable',
                'production_MeV': 343.810, 'formation': 'Silicon burning / s-process'
            },
            'Calcium (Ca-40)': {
                'Z': 20, 'N': 20, 'BE': 342.052, 'BE_per_A': 8.551, 'SEP_n': 15.64, 'SEP_p': 8.33,
                'shells': [2, 8, 18, 12], 'magic': True, 'stability': 'stable',
                'production_MeV': 342.052,
                'formation': 'Silicon burning'
            },
            'Iron (Fe-56)': {
                'Z': 26, 'N': 30, 'BE': 492.254, 'BE_per_A': 8.790, 'SEP_n': 11.20, 'SEP_p': 7.65,
                'shells': [2, 8, 14, 26, 6], 'magic': False, 'stability': 'stable (peak)',
                'production_MeV': 492.254, 'formation': 'Silicon burning / photodisintegration equilibrium'
            },
            'Nickel (Ni-58)': {
                'Z': 28, 'N': 30, 'BE': 506.459, 'BE_per_A': 8.732, 'SEP_n': 12.21, 'SEP_p': 7.76,
                'shells': [2, 8, 18, 28, 2], 'magic': True, 'stability': 'stable',
                'production_MeV': 506.459, 'formation': 'Silicon burning endpoint'
            },
            'Copper (Cu-63)': {
                'Z': 29, 'N': 34, 'BE': 551.385, 'BE_per_A': 8.752, 'SEP_n': 10.85, 'SEP_p': 6.12,
                'shells': [2, 8, 18, 29, 6], 'magic': False, 'stability': 'stable',
                'production_MeV': 551.385, 'formation': 's-process neutron capture'
            },
            'Zinc (Zn-64)': {
                'Z': 30, 'N': 34, 'BE': 559.098, 'BE_per_A': 8.736, 'SEP_n': 11.86, 'SEP_p': 7.71,
                'shells': [2, 8, 18, 30], 'magic': False, 'stability': 'stable',
                'production_MeV': 559.098, 'formation': 's-process'
            },
            'Silver (Ag-107)': {
                'Z': 47, 'N': 60, 'BE': 915.285, 'BE_per_A': 8.551, 'SEP_n': 9.56, 'SEP_p': 5.22,
                'shells': [2, 8, 18, 32, 47], 'magic': False, 'stability': 'stable',
                'production_MeV': 915.285, 'formation': 's-process / r-process'
            },
            'Tin (Sn-120)': {
                'Z': 50, 'N': 70, 'BE': 1020.510, 'BE_per_A': 8.504, 'SEP_n': 9.10, 'SEP_p': 6.48,
                'shells': [2, 8, 18, 32, 50, 10], 'magic': True, 'stability': 'stable',
                'production_MeV': 1020.510, 'formation': 's-process (magic Z=50)'
            },
            'Gold (Au-197)': {
                'Z': 79, 'N': 118, 'BE': 1559.399, 'BE_per_A': 7.916, 'SEP_n': 8.07, 'SEP_p': 4.87,
                'shells': [2, 8, 18, 32, 50, 79, 8], 'magic': False, 'stability': 'stable',
                'production_MeV': 1559.399, 'formation': 'r-process (neutron star mergers)'
            },
            'Lead (Pb-208)': {
                'Z': 82, 'N': 126, 'BE': 1636.431, 'BE_per_A': 7.868, 'SEP_n': 7.37, 'SEP_p': 8.01,
                'shells': [2, 8, 18, 32, 50, 82, 16], 'magic': True, 'stability': 'stable (doubly magic)',
                'production_MeV': 1636.431, 'formation': 's-process endpoint (Z=82, N=126 magic)'
            },
            'Uranium (U-238)': {
                'Z': 92, 'N': 146, 'BE': 1801.694, 'BE_per_A': 7.570, 'SEP_n': 6.15, 'SEP_p': 5.49,
                'shells': [2, 8, 18, 32, 50, 92, 46], 'magic': False, 'stability': 'radioactive (α-decay)',
                'production_MeV': 1801.694, 'formation': 'r-process (supernovae/mergers)'
            },
            # Additional isotopes - Unstable/Exotic
            'Deuterium (H-2)': {
                'Z': 1, 'N': 1, 'BE': 2.224, 'BE_per_A': 1.112, 'SEP_n': 2.22, 'SEP_p': 0,
                'shells': [2], 'magic': False, 'stability': 'stable',
                'production_MeV': 2.224, 'formation': 'Big Bang nucleosynthesis'
            },
            'Tritium (H-3)': {
                'Z': 1, 'N': 2, 'BE': 8.482, 'BE_per_A': 2.827, 'SEP_n': 6.26, 'SEP_p': 0,
                'shells': [3], 'magic': False, 'stability': 'radioactive (β-decay, t½=12.3y)',
                'production_MeV': 8.482, 'formation': 'Cosmic ray spallation / fusion reactors'
            },
            'Helium (He-3)': {
                'Z': 2, 'N': 1, 'BE': 7.718, 'BE_per_A': 2.573, 'SEP_n': 5.49, 'SEP_p': 7.72,
                'shells': [3], 'magic': False, 'stability': 'stable',
                'production_MeV': 7.718, 'formation': 'Big Bang / tritium decay'
            },
            'Beryllium (Be-9)': {
                'Z': 4, 'N': 5, 'BE': 58.165, 'BE_per_A': 6.463, 'SEP_n': 1.67, 'SEP_p': 16.89,
                'shells': [2, 4, 3], 'magic': False, 'stability': 'stable',
                'production_MeV': 58.165, 'formation': 'Cosmic ray spallation'
            },
            'Lithium (Li-7)': {
                'Z': 3, 'N': 4, 'BE': 39.245, 'BE_per_A': 5.606, 'SEP_n': 7.25, 'SEP_p': 10.95,
                'shells': [2, 3, 2], 'magic': False, 'stability': 'stable',
                'production_MeV': 39.245, 'formation': 'Big Bang nucleosynthesis'
            },
            'Boron (B-11)': {
                'Z': 5, 'N': 6, 'BE': 76.205, 'BE_per_A': 6.928, 'SEP_n': 11.45, 'SEP_p': 11.23,
                'shells': [2, 4, 5], 'magic': False, 'stability': 'stable',
                'production_MeV': 76.205, 'formation': 'Cosmic ray spallation'
            },
            'Neon (Ne-20)': {
                'Z': 10, 'N': 10, 'BE': 160.645, 'BE_per_A': 8.032, 'SEP_n': 16.88, 'SEP_p': 12.84,
                'shells': [2, 8, 10], 'magic': True, 'stability': 'stable',
                'production_MeV': 160.645, 'formation': 'Carbon fusion in stars'
            },
            'Chromium (Cr-52)': {
                'Z': 24, 'N': 28, 'BE': 456.348, 'BE_per_A': 8.776, 'SEP_n': 12.04, 'SEP_p': 7.94,
                'shells': [2, 8, 14, 24, 4], 'magic': False, 'stability': 'stable',
                'production_MeV': 456.348, 'formation': 'Silicon burning'
            },
            'Cobalt (Co-59)': {
                'Z': 27, 'N': 32, 'BE': 517.309, 'BE_per_A': 8.768, 'SEP_n': 10.45, 'SEP_p': 7.45,
                'shells': [2, 8, 14, 27, 8], 'magic': False, 'stability': 'stable',
                'production_MeV': 517.309, 'formation': 's-process neutron capture'
            },
            'Strontium (Sr-88)': {
                'Z': 38, 'N': 50, 'BE': 768.473, 'BE_per_A': 8.733, 'SEP_n': 11.11, 'SEP_p': 6.08,
                'shells': [2, 8, 18, 32, 38], 'magic': True, 'stability': 'stable',
                'production_MeV': 768.473, 'formation': 's-process (N=50 magic)'
            },
            'Zirconium (Zr-90)': {
                'Z': 40, 'N': 50, 'BE': 783.893, 'BE_per_A': 8.710, 'SEP_n': 7.20, 'SEP_p': 8.22,
                'shells': [2, 8, 18, 32, 40], 'magic': True, 'stability': 'stable',
                'production_MeV': 783.893, 'formation': 's-process (N=50 magic)'
            },
            'Barium (Ba-138)': {
                'Z': 56, 'N': 82, 'BE': 1172.844, 'BE_per_A': 8.499, 'SEP_n': 8.61, 'SEP_p': 5.17,
                'shells': [2, 8, 18, 32, 50, 56], 'magic': True, 'stability': 'stable',
                'production_MeV': 1172.844, 'formation': 's-process (N=82 magic)'
            },
            'Platinum (Pt-195)': {
                'Z': 78, 'N': 117, 'BE': 1543.805, 'BE_per_A': 7.917, 'SEP_n': 8.03, 'SEP_p': 4.75,
                'shells': [2, 8, 18, 32, 50, 78, 7], 'magic': False, 'stability': 'stable',
                'production_MeV': 1543.805, 'formation': 's/r-process'
            },
            'Thorium (Th-232)': {
                'Z': 90, 'N': 142, 'BE': 1766.686, 'BE_per_A': 7.615, 'SEP_n': 6.44, 'SEP_p': 5.52,
                'shells': [2, 8, 18, 32, 50, 90, 42], 'magic': False, 'stability': 'radioactive (α-decay, t½=14Gy)',
                'production_MeV': 1766.686, 'formation': 'r-process'
            },
            'Plutonium (Pu-239)': {
                'Z': 94, 'N': 145, 'BE': 1806.460, 'BE_per_A': 7.560, 'SEP_n': 6.53, 'SEP_p': 5.24,
                'shells': [2, 8, 18, 32, 50, 94, 45], 'magic': False, 'stability': 'radioactive (α-decay, t½=24ky)',
                'production_MeV': 1806.460, 'formation': 'Neutron capture in reactors'
            },
            'Uranium (U-235)': {
                'Z': 92, 'N': 143, 'BE': 1783.870, 'BE_per_A': 7.591, 'SEP_n': 5.30, 'SEP_p': 5.41,
                'shells': [2, 8, 18, 32, 50, 92, 43], 'magic': False, 'stability': 'radioactive (α-decay, t½=704My)',
                'production_MeV': 1783.870, 'formation': 'r-process (fissile)'
            },
            'Radium (Ra-226)': {
                'Z': 88, 'N': 138, 'BE': 1736.725, 'BE_per_A': 7.685, 'SEP_n': 5.52, 'SEP_p': 6.15,
                'shells': [2, 8, 18, 32, 50, 88, 38], 'magic': False, 'stability': 'radioactive (α-decay, t½=1600y)',
                'production_MeV': 1736.725, 'formation': 'U-238 decay chain'
            },
            'Polonium (Po-210)': {
                'Z': 84, 'N': 126, 'BE': 1645.174, 'BE_per_A': 7.834, 'SEP_n': 5.40, 'SEP_p': 7.54,
                'shells': [2, 8, 18, 32, 50, 84, 16], 'magic': True, 'stability': 'radioactive (α-decay, t½=138d)',
                'production_MeV': 1645.174, 'formation': 'U/Th decay chains (N=126 magic)'
            },
            'Bismuth (Bi-209)': {
                'Z': 83, 'N': 126, 'BE': 1640.238, 'BE_per_A': 7.848, 'SEP_n': 7.46, 'SEP_p': 3.80,
                'shells': [2, 8, 18, 32, 50, 83, 16], 'magic': True, 'stability': 'very long-lived (α-decay, t½=2×10¹⁹y)',
                'production_MeV': 1640.238, 'formation': 's-process endpoint (N=126 magic)'
            }
        }

        # Molecular and compound combinations
        self.molecular_data = {
            'H2 (Hydrogen gas)': {
                'formula': 'H2', 'atoms': [('Hydrogen (H-1)', 2)],
                'bond_energy': 4.52, 'type': 'molecule',
                'description': 'Diatomic hydrogen - simplest molecule'
            },
            'H2O (Water)': {
                'formula': 'H2O', 'atoms': [('Hydrogen (H-1)', 2), ('Oxygen (O-16)', 1)],
                'bond_energy': 9.51, 'type': 'molecule',
                'description': 'Water molecule - essential for life'
            },
            'CO2 (Carbon dioxide)': {
                'formula': 'CO2', 'atoms': [('Carbon (C-12)', 1), ('Oxygen (O-16)', 2)],
                'bond_energy': 16.3, 'type': 'molecule',
                'description': 'Carbon dioxide - greenhouse gas'
            },
            'O2 (Oxygen gas)': {
                'formula': 'O2', 'atoms': [('Oxygen (O-16)', 2)],
                'bond_energy': 5.15, 'type': 'molecule',
                'description': 'Diatomic oxygen - essential for respiration'
            },
            'N2 (Nitrogen gas)': {
                'formula': 'N2', 'atoms': [('Nitrogen (N-14)', 2)],
                'bond_energy': 9.79, 'type': 'molecule',
                'description': 'Diatomic nitrogen - 78% of atmosphere'
            },
            'CH4 (Methane)': {
                'formula': 'CH4', 'atoms': [('Carbon (C-12)', 1), ('Hydrogen (H-1)', 4)],
                'bond_energy': 17.4, 'type': 'molecule',
                'description': 'Methane - simplest hydrocarbon'
            },
            'NH3 (Ammonia)': {
                'formula': 'NH3', 'atoms': [('Nitrogen (N-14)', 1), ('Hydrogen (H-1)', 3)],
                'bond_energy': 12.5, 'type': 'molecule',
                'description': 'Ammonia - important for fertilizers'
            },
            'C6H12O6 (Glucose)': {
                'formula': 'C6H12O6', 'atoms': [('Carbon (C-12)', 6), ('Hydrogen (H-1)', 12), ('Oxygen (O-16)', 6)],
                'bond_energy': 67.2, 'type': 'molecule',
                'description': 'Glucose - primary energy source for cells'
            },
            'NaCl (Salt)': {
                'formula': 'NaCl', 'atoms': [('Sodium (Na-23)', 1), ('Chlorine (Cl-35)', 1)],
                'bond_energy': 3.28, 'type': 'ionic',
                'description': 'Sodium chloride - table salt'
            },
            'CaCO3 (Limestone)': {
                'formula': 'CaCO3', 'atoms': [('Calcium (Ca-40)', 1), ('Carbon (C-12)', 1), ('Oxygen (O-16)', 3)],
                'bond_energy': 12.1, 'type': 'ionic',
                'description': 'Calcium carbonate - limestone, marble'
            },
            'H2SO4 (Sulfuric acid)': {
                'formula': 'H2SO4', 'atoms': [('Hydrogen (H-1)', 2), ('Sulfur (S-32)', 1), ('Oxygen (O-16)', 4)],
                'bond_energy': 23.8, 'type': 'molecule',
                'description': 'Sulfuric acid - strong mineral acid'
            },
            'NaOH (Sodium hydroxide)': {
                'formula': 'NaOH', 'atoms': [('Sodium (Na-23)', 1), ('Oxygen (O-16)', 1), ('Hydrogen (H-1)', 1)],
                'bond_energy': 8.4, 'type': 'ionic',
                'description': 'Sodium hydroxide - caustic soda'
            },
            'Fe2O3 (Iron oxide)': {
                'formula': 'Fe2O3', 'atoms': [('Iron (Fe-56)', 2), ('Oxygen (O-16)', 3)],
                'bond_energy': 16.7, 'type': 'ionic',
                'description': 'Iron(III) oxide - rust'
            },
            'D+T→He4+n (Fusion)': {
                'formula': 'D+T→He4+n', 'atoms': [('Hydrogen (H-1)', 1), ('Helium (He-4)', 1)],
                'bond_energy': 17.6, 'type': 'fusion',
                'description': 'Deuterium-Tritium fusion - releases 17.6 MeV',
                'reaction': 'D(2,1) + T(3,1) → He-4(4,2) + n(1,0) + 17.6 MeV'
            },
            'H+H→D+e+ν (pp-chain)': {
                'formula': 'H+H→D', 'atoms': [('Hydrogen (H-1)', 2)],
                'bond_energy': 1.44, 'type': 'fusion',
                'description': 'Proton-proton chain step 1 - solar fusion',
                'reaction': 'p + p → D + e+ + νe + 1.44 MeV'
            },
            '3He+4He→7Be (Stellar)': {
                'formula': '3He+4He', 'atoms': [('Helium (He-4)', 2)],
                'bond_energy': 1.59, 'type': 'fusion',
                'description': 'Helium fusion in stars - pp-III branch',
                'reaction': 'He-3 + He-4 → Be-7 + γ + 1.59 MeV'
            },
            'U-235 fission fragments': {
                'formula': 'U-235 fission', 'atoms': [('Uranium (U-238)', 1)],
                'bond_energy': 200.0, 'type': 'fission',
                'description': 'U-235 fission - typical fragments Kr-92 + Ba-141',
                'reaction': 'U-235 + n → Kr-92 + Ba-141 + 3n + ~200 MeV'
            },
            'Pu-239 fission products': {
                'formula': 'Pu-239 fission', 'atoms': [('Uranium (U-238)', 1)],
                'bond_energy': 207.0, 'type': 'fission',
                'description': 'Pu-239 fission - nuclear reactor fuel',
                'reaction': 'Pu-239 + n → fission products + ~207 MeV'
            }
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        # Title
        title = tk.Label(self.root, text="⚛ SUBSET SUM NUCLEAR SIMULATOR ⚛", 
                        font=('Arial', 20, 'bold'), bg='#1a1a2e', fg='#00ff41')
        title.pack(pady=10)
        
        # Control Panel
        control_frame = tk.Frame(self.root, bg='#16213e')
        control_frame.pack(fill='x', padx=10, pady=5)
        
        # Parameters
        param_frame = tk.Frame(control_frame, bg='#16213e')
        param_frame.pack(side='left', padx=10)
        
        tk.Label(param_frame, text="Set Size:", bg='#16213e', fg='white').grid(row=0, column=0, padx=5)
        self.size_var = tk.StringVar(value="590")
        tk.Entry(param_frame, textvariable=self.size_var, width=10, bg='#0f3460', fg='white').grid(row=0, column=1, padx=5)
        
        tk.Label(param_frame, text="Subset Size:", bg='#16213e', fg='white').grid(row=1, column=0, padx=5)
        self.subset_var = tk.StringVar(value="8")
        tk.Entry(param_frame, textvariable=self.subset_var, width=10, bg='#0f3460', fg='white').grid(row=1, column=1, padx=5)
        
        tk.Label(param_frame, text="Atom Type:", bg='#16213e', fg='white').grid(row=2, column=0, padx=5)
        self.atom_var = tk.StringVar(value="Custom")
        self.atom_dropdown = ttk.Combobox(param_frame, textvariable=self.atom_var, width=20, state='readonly')
        self.atom_dropdown['values'] = (
            'Custom',
            '--- SINGLE ATOMS ---',
            'Hydrogen (H-1)',
            'Deuterium (H-2)',
            'Tritium (H-3) [Radioactive]',
            'Helium (He-3)',
            'Helium (He-4) [Magic]',
            'Lithium (Li-7)',
            'Beryllium (Be-9)',
            'Boron (B-11)',
            'Carbon (C-12)',
            'Nitrogen (N-14)',
            'Oxygen (O-16) [Magic]',
            'Neon (Ne-20) [Magic]',
            'Sodium (Na-23)',
            'Magnesium (Mg-24)',
            'Aluminum (Al-27)',
            'Silicon (Si-28) [Magic]',
            'Phosphorus (P-31)',
            'Sulfur (S-32)',
            'Chlorine (Cl-35)',
            'Argon (Ar-40)',
            'Calcium (Ca-40) [Magic]',
            'Chromium (Cr-52)',
            'Iron (Fe-56) [Peak BE]',
            'Cobalt (Co-59)',
            'Nickel (Ni-58) [Magic]',
            'Copper (Cu-63)',
            'Zinc (Zn-64)',
            'Strontium (Sr-88) [Magic]',
            'Zirconium (Zr-90) [Magic]',
            'Silver (Ag-107)',
            'Tin (Sn-120) [Magic]',
            'Barium (Ba-138) [Magic]',
            'Platinum (Pt-195)',
            'Gold (Au-197)',
            'Lead (Pb-208) [Doubly Magic]',
            'Bismuth (Bi-209) [Magic]',
            'Polonium (Po-210) [Radioactive]',
            'Radium (Ra-226) [Radioactive]',
            'Thorium (Th-232) [Radioactive]',
            'Uranium (U-235) [Fissile]',
            'Uranium (U-238) [Radioactive]',
            'Plutonium (Pu-239) [Fissile]',
            '--- MOLECULES ---',
            'H2 (Hydrogen gas)',
            'H2O (Water)',
            'CO2 (Carbon dioxide)',
            'O2 (Oxygen gas)',
            'N2 (Nitrogen gas)',
            'CH4 (Methane)',
            'NH3 (Ammonia)',
            'C6H12O6 (Glucose)',
            '--- COMPOUNDS ---',
            'NaCl (Salt)',
            'CaCO3 (Limestone)',
            'H2SO4 (Sulfuric acid)',
            'NaOH (Sodium hydroxide)',
            'Fe2O3 (Iron oxide)',
            '--- FUSION REACTIONS ---',
            'D+T→He4+n (Fusion)',
            'H+H→D+e+ν (pp-chain)',
            '3He+4He→7Be (Stellar)',
            '--- FISSION PRODUCTS ---',
            'U-235 fission fragments',
            'Pu-239 fission products'
        )
        self.atom_dropdown.grid(row=2, column=1, padx=5)
        self.atom_dropdown.bind('<<ComboboxSelected>>', self.on_atom_select)
        
        # Buttons
        btn_frame = tk.Frame(control_frame, bg='#16213e')
        btn_frame.pack(side='left', padx=20)
        
        self.gen_btn = tk.Button(btn_frame, text="⚡ Generate Problem", command=self.generate_problem,
                                bg='#e94560', fg='white', font=('Arial', 10, 'bold'), width=20)
        self.gen_btn.grid(row=0, column=0, padx=5, pady=5)
        
        self.solve_btn = tk.Button(btn_frame, text="🔬 Solve (Exact DP)", command=self.solve_exact,
                                   bg='#00d4ff', fg='black', font=('Arial', 10, 'bold'), width=20)
        self.solve_btn.grid(row=0, column=1, padx=5, pady=5)
        
        self.anneal_btn = tk.Button(btn_frame, text="🌡 Solve (Annealing)", command=self.solve_annealing,
                                    bg='#f97068', fg='white', font=('Arial', 10, 'bold'), width=20)
        self.anneal_btn.grid(row=1, column=0, padx=5, pady=5)
        
        self.reset_btn = tk.Button(btn_frame, text="🔄 Reset", command=self.reset,
                                   bg='#533483', fg='white', font=('Arial', 10, 'bold'), width=20)
        self.reset_btn.grid(row=1, column=1, padx=5, pady=5)
        
        # Status Panel
        status_frame = tk.Frame(self.root, bg='#16213e', relief='ridge', bd=2)
        status_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(status_frame, text="STATUS:", bg='#16213e', fg='#00ff41', 
                font=('Arial', 12, 'bold')).pack(side='left', padx=10)
        
        self.status_label = tk.Label(status_frame, text="Ready to generate problem", 
                                     bg='#16213e', fg='white', font=('Arial', 11))
        self.status_label.pack(side='left', padx=10)
        
        # Main Content Area
        content_frame = tk.Frame(self.root, bg='#1a1a2e')
        content_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Left Panel - Problem Data
        left_frame = tk.LabelFrame(content_frame, text="Nuclear Energy Orbitals", 
                                  bg='#16213e', fg='#00ff41', font=('Arial', 12, 'bold'))
        left_frame.pack(side='left', fill='both', expand=True, padx=5)
        
        self.data_text = scrolledtext.ScrolledText(left_frame, width=40, height=25, 
                                                   bg='#0f3460', fg='#00ff41', 
                                                   font=('Courier', 9))
        self.data_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Middle Panel - Visualization
        mid_frame = tk.LabelFrame(content_frame, text="Energy Distribution", 
                                 bg='#16213e', fg='#00ff41', font=('Arial', 12, 'bold'))
        mid_frame.pack(side='left', fill='both', expand=True, padx=5)
        
        self.canvas = tk.Canvas(mid_frame, width=300, height=500, bg='#0f3460', highlightthickness=0)
        self.canvas.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Right Panel - Solution & Logs
        right_frame = tk.LabelFrame(content_frame, text="Solution & Logs", 
                                   bg='#16213e', fg='#00ff41', font=('Arial', 12, 'bold'))
        right_frame.pack(side='left', fill='both', expand=True, padx=5)
        
        self.log_text = scrolledtext.ScrolledText(right_frame, width=40, height=25, 
                                                 bg='#0f3460', fg='white', 
                                                 font=('Courier', 9))
        self.log_text.pack(fill='both', expand=True, padx=5, pady=5)
        
    def add_log(self, message, color='white'):
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert('end', f"[{timestamp}] {message}\n", color)
        self.log_text.tag_config('white', foreground='white')
        self.log_text.tag_config('green', foreground='#00ff41')
        self.log_text.tag_config('cyan', foreground='#00d4ff')
        self.log_text.tag_config('yellow', foreground='#f9ca24')
        self.log_text.tag_config('red', foreground='#e94560')
        self.log_text.see('end')
        self.root.update()
        
    def on_atom_select(self, event=None):
        atom = self.atom_var.get()
        
        # Skip separator lines
        if atom.startswith('---'):
            self.atom_var.set('Custom')
            return
        
        # Remove tags like [Magic] for lookup
        atom_clean = atom.split(' [')[0]
        
        if atom == 'Custom':
            self.size_var.set("590")
            self.subset_var.set("8")
            self.add_log("Custom mode selected", 'cyan')
        elif atom_clean in self.molecular_data:
            # Handle molecular/compound combinations
            mol = self.molecular_data[atom_clean]
            
            self.add_log(f"\n⚛️ MOLECULAR SYSTEM LOADED: {atom_clean}", 'cyan')
            self.add_log(f"  Formula: {mol['formula']}", 'white')
            self.add_log(f"  Type: {mol['type'].upper()}", 'yellow')
            self.add_log(f"  Description: {mol['description']}", 'white')
            
            # Calculate total nuclear binding energy
            total_be = 0
            total_nucleons = 0
            atom_list = []
            
            for atom_name, count in mol['atoms']:
                if atom_name in self.atomic_data:
                    data = self.atomic_data[atom_name]
                    total_be += data['BE'] * count
                    total_nucleons += (data['Z'] + data['N']) * count
                    atom_list.append(f"{count}×{atom_name}")
            
            self.add_log(f"\n  Atomic composition:", 'cyan')
            for item in atom_list:
                self.add_log(f"    • {item}", 'white')
            
            self.add_log(f"\n  Nuclear binding energy: {total_be:.3f} MeV", 'green')
            
            if mol['type'] in ['molecule', 'ionic']:
                self.add_log(f"  Chemical bond energy: {mol['bond_energy']} eV", 'yellow')
                self.add_log(f"    (Note: Bond energy ≪ nuclear BE)", 'white')
            elif mol['type'] == 'fusion':
                self.add_log(f"  Energy released: {mol['bond_energy']} MeV", 'green')
                self.add_log(f"  Reaction: {mol['reaction']}", 'white')
            elif mol['type'] == 'fission':
                self.add_log(f"  Energy released: {mol['bond_energy']} MeV", 'green')
                self.add_log(f"  Reaction: {mol['reaction']}", 'white')
            
            # Set parameters based on composition
            self.size_var.set(str(total_nucleons * 10))
            self.subset_var.set(str(len(mol['atoms']) * 2))
            
            self.status_label.config(text=f"{mol['formula']} - {mol['type']}")
            
        else:
            # Handle single atoms
            data = self.atomic_data[atom_clean]
            A = data['Z'] + data['N']
            self.size_var.set(str(A * 10))
            self.subset_var.set(str(len(data['shells'])))
            
            self.add_log(f"⚛ {atom_clean} NUCLEUS LOADED", 'cyan')
            self.add_log(f"  Protons (Z): {data['Z']}, Neutrons (N): {data['N']}, Mass (A): {A}", 'white')
            self.add_log(f"  Total Binding Energy: {data['BE']:.3f} MeV", 'green')
            self.add_log(f"  BE per nucleon: {data['BE_per_A']:.3f} MeV/A", 'green')
            self.add_log(f"  Last neutron separation: {data['SEP_n']:.2f} MeV", 'yellow')
            self.add_log(f"  Last proton separation: {data['SEP_p']:.2f} MeV", 'yellow')
            self.add_log(f"  Nuclear shells: {data['shells']}", 'cyan')
            
            if data['magic']:
                self.add_log(f"  ✨ MAGIC NUCLEUS - Enhanced stability!", 'green')
            
            self.add_log(f"  Formation: {data['formation']}", 'white')
            self.add_log(f"  Production energy required: {data['production_MeV']:.3f} MeV", 'cyan')
            self.add_log(f"    (Energy to assemble from {data['Z']} protons + {data['N']} neutrons)", 'white')
            
            self.status_label.config(text=f"{atom_clean} - BE={data['BE']:.1f} MeV")
            
    def generate_problem(self):
        try:
            set_size = int(self.size_var.get())
            subset_size = int(self.subset_var.get())
            atom = self.atom_var.get()
            atom_clean = atom.split(' [')[0]
            
            self.add_log(f"\n{'='*60}", 'white')
            self.add_log(f"⚛ GENERATING NUCLEAR ENERGY PROBLEM", 'cyan')
            self.add_log(f"{'='*60}", 'white')
            
            if atom_clean in self.molecular_data:
                # Handle molecular/compound combinations
                mol = self.molecular_data[atom_clean]
                
                self.add_log(f"\n🧪 MOLECULAR SYSTEM: {mol['formula']}", 'cyan')
                self.add_log(f"  Type: {mol['type'].upper()}", 'yellow')
                self.add_log(f"  {mol['description']}", 'white')
                
                # Combine nuclear energies from constituent atoms
                total_be = 0
                all_numbers = []
                
                self.add_log(f"\n⚛️ CONSTITUENT NUCLEI:", 'cyan')
                
                for atom_name, count in mol['atoms']:
                    if atom_name in self.atomic_data:
                        data = self.atomic_data[atom_name]
                        total_be += data['BE'] * count
                        
                        self.add_log(f"  {count}× {atom_name}:", 'white')
                        self.add_log(f"     Z={data['Z']}, N={data['N']}, BE={data['BE']:.3f} MeV", 'white')
                        
                        # Generate orbitals for each atom
                        base_energy = int(data['BE_per_A'] * 100)
                        for shell_idx, shell_count in enumerate(data['shells']):
                            shell_energy_factor = (len(data['shells']) - shell_idx) / len(data['shells'])
                            shell_energy = int(base_energy * shell_energy_factor * (1.0 + 0.2 * shell_idx))
                            sep_energy_avg = (data['SEP_n'] + data['SEP_p']) / 2
                            splitting = int(sep_energy_avg * 10)
                            
                            for _ in range(shell_count * count * 5):  # 5 orbitals per shell per atom
                                variation = random.randint(-splitting, splitting)
                                orbital_energy = max(1, shell_energy + variation)
                                all_numbers.append(orbital_energy)
                
                self.add_log(f"\n⚡ TOTAL SYSTEM ENERGETICS:", 'yellow')
                self.add_log(f"  Combined nuclear BE: {total_be:.3f} MeV", 'green')
                
                if mol['type'] in ['molecule', 'ionic']:
                    self.add_log(f"  Chemical bond energy: {mol['bond_energy']} eV", 'yellow')
                    self.add_log(f"  Ratio (Nuclear/Chemical): {(total_be*1e6)/mol['bond_energy']:.2e}×", 'white')
                elif mol['type'] == 'fusion':
                    self.add_log(f"  Fusion energy release: {mol['bond_energy']} MeV", 'green')
                    self.add_log(f"  Q-value: {mol['bond_energy']} MeV", 'green')
                    self.add_log(f"  Reaction: {mol['reaction']}", 'white')
                elif mol['type'] == 'fission':
                    self.add_log(f"  Fission energy release: {mol['bond_energy']} MeV", 'green')
                    self.add_log(f"  Q-value: {mol['bond_energy']} MeV", 'green')
                    self.add_log(f"  Reaction: {mol['reaction']}", 'white')
                
                # Pad to set_size
                while len(all_numbers) < set_size:
                    continuum = random.randint(100, 1000)
                    all_numbers.append(continuum)
                
                self.numbers = all_numbers[:set_size]
                
                self.add_log(f"\n🔢 GENERATED ORBITALS:", 'cyan')
                self.add_log(f"  Total orbitals: {len(self.numbers)}", 'white')
                self.add_log(f"  Energy range: {min(self.numbers)} - {max(self.numbers)} keV", 'white')
                
            elif atom != 'Custom':
                # Handle single atoms
                data = self.atomic_data[atom_clean]
                A = data['Z'] + data['N']
                
                self.add_log(f"\n🔬 ISOTOPE: {atom_clean}", 'cyan')
                self.add_log(f"  Configuration: Z={data['Z']}, N={data['N']}, A={A}", 'white')
                self.add_log(f"  Stability: {data['stability']}", 'green')
                self.add_log(f"\n⚡ ENERGETICS:", 'yellow')
                self.add_log(f"  Total Binding Energy: {data['BE']:.3f} MeV", 'green')
                self.add_log(f"  Production Energy: {data['production_MeV']:.3f} MeV", 'cyan')
                self.add_log(f"    (Required to assemble nucleus from free nucleons)", 'white')
                self.add_log(f"  Average BE/nucleon: {data['BE_per_A']:.3f} MeV", 'white')
                
                if data['magic']:
                    self.add_log(f"\n✨ MAGIC NUMBER NUCLEUS - EXTRA STABLE", 'green')
                    self.add_log(f"    Enhanced binding from closed shells", 'white')
                
                self.add_log(f"\n🌟 FORMATION PROCESS:", 'yellow')
                self.add_log(f"  {data['formation']}", 'white')
                
                self.add_log(f"\n🔢 NUCLEAR SHELL MODEL:", 'cyan')
                self.add_log(f"  Shells: {data['shells']}", 'white')
                self.add_log(f"  Neutron separation energy: {data['SEP_n']:.2f} MeV", 'white')
                self.add_log(f"  Proton separation energy: {data['SEP_p']:.2f} MeV", 'white')
                
                # Generate energies based on nuclear shell model
                self.add_log(f"\n⚙️ Generating {set_size} orbital energies...", 'cyan')
                
                base_energy = int(data['BE_per_A'] * 100)
                self.numbers = []
                
                for shell_idx, shell_count in enumerate(data['shells']):
                    shell_energy_factor = (len(data['shells']) - shell_idx) / len(data['shells'])
                    shell_energy = int(base_energy * shell_energy_factor * (1.0 + 0.2 * shell_idx))
                    sep_energy_avg = (data['SEP_n'] + data['SEP_p']) / 2
                    splitting = int(sep_energy_avg * 10)
                    
                    for _ in range(shell_count * 10):
                        variation = random.randint(-splitting, splitting)
                        orbital_energy = max(1, shell_energy + variation)
                        self.numbers.append(orbital_energy)
                
                while len(self.numbers) < set_size:
                    continuum_energy = random.randint(base_energy // 3, base_energy * 2)
                    self.numbers.append(continuum_energy)
                    
                self.numbers = self.numbers[:set_size]
                
                self.add_log(f"  Energy range: {min(self.numbers)} - {max(self.numbers)} keV", 'white')
                self.add_log(f"  Mean orbital energy: {sum(self.numbers)/len(self.numbers):.1f} keV", 'white')
                
            else:
                # Custom random generation
                self.add_log(f"  Custom mode: Generating {set_size} random energies", 'white')
                self.numbers = [random.randint(1, 11500) for _ in range(set_size)]
            
            self.status_label.config(text="Selecting subset configuration...")
            
            # Generate target subset
            self.generated_subset = random.sample(self.numbers, subset_size)
            self.target = sum(self.generated_subset)
            
            self.add_log(f"\n🎯 TARGET CONFIGURATION:", 'yellow')
            self.add_log(f"  Selected {subset_size} orbitals", 'white')
            self.add_log(f"  Target binding contribution: {self.target} keV", 'green')
            self.add_log(f"  Configuration: {sorted(self.generated_subset)[:5]}{'...' if len(self.generated_subset) > 5 else ''}", 'white')
            
            # Display data
            self.data_text.delete(1.0, 'end')
            self.data_text.insert('end', f"SET SIZE: {len(self.numbers)}\n", 'bold')
            self.data_text.insert('end', f"TARGET SUM: {self.target}\n\n", 'bold')
            self.data_text.insert('end', f"Generated Subset ({len(self.generated_subset)} orbitals):\n")
            self.data_text.insert('end', f"{sorted(self.generated_subset)}\n\n")
            self.data_text.insert('end', f"First 50 energies:\n{self.numbers[:50]}\n")
            
            self.add_log(f"✓ Generated subset: {sorted(self.generated_subset)[:3]}... (size={len(self.generated_subset)})", 'green')
            self.add_log(f"✓ Target binding energy: {self.target}", 'green')
            
            self.visualize_distribution()
            self.status_label.config(text=f"Problem generated: {set_size} orbitals, target={self.target}")
            self.solution = None
            
        except Exception as e:
            self.add_log(f"✗ Error: {str(e)}", 'red')
            
    def visualize_distribution(self):
        self.canvas.delete('all')
        if not self.numbers:
            return
            
        width = self.canvas.winfo_width() or 300
        height = self.canvas.winfo_height() or 500
        
        # Create histogram
        max_val = max(self.numbers)
        bins = 20
        hist = [0] * bins
        
        for num in self.numbers:
            bin_idx = min(int((num / max_val) * (bins - 1)), bins - 1)
            hist[bin_idx] += 1
            
        max_count = max(hist) if max(hist) > 0 else 1
        bar_width = width / bins
        
        for i, count in enumerate(hist):
            bar_height = (count / max_count) * (height - 40)
            x0 = i * bar_width
            y0 = height - bar_height - 20
            x1 = (i + 1) * bar_width - 2
            y1 = height - 20
            
            color = '#00ff41' if self.solution and any(n in self.solution for n in self.numbers) else '#00d4ff'
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline='#1a1a2e')
        
        # Labels
        self.canvas.create_text(width/2, 10, text="Energy Distribution", 
                               fill='white', font=('Arial', 10, 'bold'))
        
    def solve_exact_dp(self):
        if self.target == 0:
            return []
        if len(self.numbers) == 0 or self.target < 0:
            return None
            
        self.add_log("🔬 Starting Exact DP Algorithm...", 'cyan')
        self.add_log(f"  Building DP table for target={self.target}...", 'white')
        
        # DP algorithm
        dp = [False] * (self.target + 1)
        dp[0] = True
        prev = [-1] * (self.target + 1)
        
        for idx, num in enumerate(self.numbers):
            if idx % 50 == 0:
                self.add_log(f"  Processing orbital {idx}/{len(self.numbers)}...", 'white')
            for s in range(self.target, num - 1, -1):
                if not dp[s] and dp[s - num]:
                    dp[s] = True
                    prev[s] = s - num
                    
        if not dp[self.target]:
            return None
            
        # Reconstruct
        self.add_log("  Reconstructing solution path...", 'white')
        subset = []
        s = self.target
        while s > 0:
            prev_s = prev[s]
            if prev_s == -1:
                break
            num = s - prev_s
            subset.append(num)
            s = prev_s
            
        return subset
        
    def solve_exact(self):
        if not self.numbers:
            self.add_log("✗ Generate a problem first!", 'red')
            return
        
        def run():
            self.running = True
            self.solve_btn.config(state='disabled')
            
            start = time.time()
            result = self.solve_exact_dp()
            elapsed = time.time() - start
            
            if result:
                self.solution = sorted(result)
                self.add_log(f"\n{'='*60}", 'white')
                self.add_log(f"✓ EXACT SOLUTION FOUND!", 'green')
                self.add_log(f"{'='*60}", 'white')
                
                # Solution details
                self.add_log(f"\n🎯 SOLUTION SUBSET:", 'cyan')
                self.add_log(f"  Orbitals selected: {len(self.solution)}", 'white')
                self.add_log(f"  Configuration: {self.solution}", 'green')
                self.add_log(f"  Total energy: {sum(self.solution)} keV", 'green')
                self.add_log(f"  Target energy: {self.target} keV", 'white')
                self.add_log(f"  Match: {'PERFECT ✓' if sum(self.solution) == self.target else 'NO'}", 'green')
                
                # Statistical analysis
                self.add_log(f"\n📊 STATISTICAL ANALYSIS:", 'yellow')
                mean_val = sum(self.solution) / len(self.solution)
                self.add_log(f"  Mean orbital energy: {mean_val:.2f} keV", 'white')
                self.add_log(f"  Min orbital: {min(self.solution)} keV", 'white')
                self.add_log(f"  Max orbital: {max(self.solution)} keV", 'white')
                self.add_log(f"  Energy range: {max(self.solution) - min(self.solution)} keV", 'white')
                
                # Nuclear physics interpretation
                atom = self.atom_var.get()
                atom_clean = atom.split(' [')[0]
                
                if atom_clean in self.molecular_data:
                    # Molecular/compound interpretation
                    mol = self.molecular_data[atom_clean]
                    self.add_log(f"\n⚛️ MOLECULAR SYSTEM INTERPRETATION:", 'cyan')
                    self.add_log(f"  System: {mol['formula']}", 'white')
                    self.add_log(f"  Type: {mol['type']}", 'white')
                    
                    # Calculate total BE from constituents
                    total_be = 0
                    for atom_name, count in mol['atoms']:
                        if atom_name in self.atomic_data:
                            total_be += self.atomic_data[atom_name]['BE'] * count
                    
                    solution_mev = sum(self.solution) / 1000.0
                    self.add_log(f"  Solution binding: {solution_mev:.3f} MeV", 'white')
                    self.add_log(f"  System total BE: {total_be:.3f} MeV", 'white')
                    
                    if mol['type'] in ['molecule', 'ionic']:
                        self.add_log(f"  Chemical bond energy: {mol['bond_energy']} eV", 'yellow')
                        self.add_log(f"  Nuclear/Chemical ratio: {(total_be*1e6/mol['bond_energy']):.2e}×", 'white')
                    elif mol['type'] == 'fusion':
                        self.add_log(f"  Fusion Q-value: {mol['bond_energy']} MeV", 'green')
                        self.add_log(f"  Selected orbitals model fusion pathway", 'white')
                    elif mol['type'] == 'fission':
                        self.add_log(f"  Fission Q-value: {mol['bond_energy']} MeV", 'green')
                        self.add_log(f"  Selected orbitals model fragment states", 'white')
                    
                elif atom != 'Custom':
                    data = self.atomic_data[atom_clean]
                    self.add_log(f"\n⚛️ NUCLEAR PHYSICS INTERPRETATION:", 'cyan')
                    self.add_log(f"  Nucleus: {atom_clean}", 'white')
                    self.add_log(f"  Selected orbitals represent {len(self.solution)}/{len(data['shells'])} shell levels", 'white')
                    
                    # Compare to actual binding energy
                    solution_mev = sum(self.solution) / 1000.0  # Convert keV to MeV
                    actual_be = data['BE']
                    ratio = (solution_mev / actual_be) * 100 if actual_be > 0 else 0
                    
                    self.add_log(f"  Solution binding: {solution_mev:.3f} MeV", 'white')
                    self.add_log(f"  Actual nucleus BE: {actual_be:.3f} MeV", 'white')
                    self.add_log(f"  Simulation scale: {ratio:.1f}% of actual", 'white')
                    
                    # Energy per nucleon
                    A = data['Z'] + data['N']
                    sim_be_per_nucleon = solution_mev / A if A > 0 else 0
                    self.add_log(f"  Simulated BE/A: {sim_be_per_nucleon:.3f} MeV/nucleon", 'white')
                    self.add_log(f"  Actual BE/A: {data['BE_per_A']:.3f} MeV/nucleon", 'white')
                    
                    # Stability analysis
                    self.add_log(f"\n🔬 STABILITY ANALYSIS:", 'yellow')
                    self.add_log(f"  Nuclear stability: {data['stability']}", 'green' if 'stable' in data['stability'] else 'red')
                    
                    if data['magic']:
                        self.add_log(f"  ✨ Magic number configuration detected!", 'green')
                        self.add_log(f"     Enhanced stability from closed shells", 'white')
                    
                    # Formation context
                    self.add_log(f"\n🌟 ASTROPHYSICAL CONTEXT:", 'cyan')
                    self.add_log(f"  Formation: {data['formation']}", 'white')
                    self.add_log(f"  Production energy: {data['production_MeV']:.3f} MeV", 'white')
                    
                    # Compare to neighboring elements
                    if data['BE_per_A'] >= 8.5:
                        self.add_log(f"  ⭐ High BE/A - Near iron peak (maximum stability)", 'green')
                    elif data['BE_per_A'] >= 8.0:
                        self.add_log(f"  ✓ Moderate BE/A - Stable configuration", 'white')
                    else:
                        self.add_log(f"  ⚠ Lower BE/A - Less tightly bound", 'yellow')
                    
                    # Shell model commentary
                    self.add_log(f"\n🔢 SHELL MODEL:", 'cyan')
                    self.add_log(f"  Nuclear shells: {data['shells']}", 'white')
                    self.add_log(f"  Last neutron separation: {data['SEP_n']:.2f} MeV", 'white')
                    self.add_log(f"  Last proton separation: {data['SEP_p']:.2f} MeV", 'white')
                    
                    sep_avg = (data['SEP_n'] + data['SEP_p']) / 2
                    if sep_avg > 12:
                        self.add_log(f"  ⚡ High separation energy - Tightly bound nucleus", 'green')
                    elif sep_avg < 8:
                        self.add_log(f"  ⚠ Low separation energy - Weakly bound outer nucleons", 'yellow')
                
                # Algorithm performance
                self.add_log(f"\n⚙️ ALGORITHM PERFORMANCE:", 'yellow')
                self.add_log(f"  Method: Exact Dynamic Programming", 'white')
                self.add_log(f"  Time elapsed: {elapsed:.3f} seconds", 'white')
                self.add_log(f"  Search space: {len(self.numbers)} orbitals", 'white')
                self.add_log(f"  DP table size: {self.target + 1} entries", 'white')
                self.add_log(f"  Complexity: O(n × target) = O({len(self.numbers)} × {self.target})", 'white')
                
                self.add_log(f"\n{'='*60}", 'white')
                
                self.status_label.config(text=f"Solution found: {len(self.solution)} orbitals, {sum(self.solution)} keV")
                self.visualize_distribution()
            else:
                self.add_log(f"\n{'='*60}", 'white')
                self.add_log("✗ No solution found", 'red')
                self.add_log(f"{'='*60}", 'white')
                self.add_log(f"\n⚠️ SOLUTION ANALYSIS:", 'yellow')
                self.add_log(f"  Target: {self.target} keV", 'white')
                self.add_log(f"  Search space: {len(self.numbers)} orbitals", 'white')
                self.add_log(f"  Energy range: {min(self.numbers)} - {max(self.numbers)} keV", 'white')
                self.add_log(f"\n  Possible reasons:", 'white')
                self.add_log(f"    • Target not achievable with subset", 'white')
                self.add_log(f"    • DP table constraints exceeded", 'white')
                self.add_log(f"    • Try Annealing method for approximation", 'white')
                self.add_log(f"\n{'='*60}", 'white')
                self.status_label.config(text="No solution exists")
                
            self.running = False
            self.solve_btn.config(state='normal')
            
        threading.Thread(target=run, daemon=True).start()
        
    def solve_annealing(self):
        if not self.numbers:
            self.add_log("✗ Generate a problem first!", 'red')
            return
        
        def run():
            self.running = True
            self.anneal_btn.config(state='disabled')
            
            self.add_log("🌡 Starting Simulated Annealing...", 'cyan')
            start = time.time()
            
            # Simplified annealing
            n = len(self.numbers)
            inclusions = [random.random() for _ in range(n)]
            
            for step in range(10000):
                current_sum = sum(inclusions[i] * self.numbers[i] for i in range(n))
                error = abs(current_sum - self.target)
                
                if step % 1000 == 0:
                    self.add_log(f"  Step {step}: error={error:.2f}", 'white')
                
                if error < 0.1:
                    break
                    
                # Update random inclusion
                i = random.randint(0, n - 1)
                force = (self.target - current_sum) / (self.numbers[i] + 1)
                inclusions[i] = max(0, min(1, inclusions[i] + force * 0.01))
            
            # Threshold to binary
            subset = [self.numbers[i] for i in range(n) if round(inclusions[i]) == 1]
            elapsed = time.time() - start
            
            if abs(sum(subset) - self.target) < 1:
                self.solution = sorted(subset)
                self.add_log(f"\n{'='*60}", 'white')
                self.add_log(f"✓ ANNEALING SOLUTION FOUND!", 'green')
                self.add_log(f"{'='*60}", 'white')
                
                # Solution details
                self.add_log(f"\n🌡️ SIMULATED ANNEALING RESULT:", 'cyan')
                self.add_log(f"  Orbitals selected: {len(self.solution)}", 'white')
                self.add_log(f"  Configuration: {self.solution[:10]}{'...' if len(self.solution) > 10 else ''}", 'green')
                self.add_log(f"  Total energy: {sum(self.solution)} keV", 'green')
                self.add_log(f"  Target energy: {self.target} keV", 'white')
                self.add_log(f"  Error: {abs(sum(self.solution) - self.target)} keV", 'yellow')
                
                # Statistical analysis
                self.add_log(f"\n📊 STATISTICAL ANALYSIS:", 'yellow')
                mean_val = sum(self.solution) / len(self.solution)
                self.add_log(f"  Mean orbital energy: {mean_val:.2f} keV", 'white')
                self.add_log(f"  Orbitals range: {min(self.solution)} - {max(self.solution)} keV", 'white')
                
                # Nuclear interpretation
                atom = self.atom_var.get()
                atom_clean = atom.split(' [')[0]
                
                if atom != 'Custom':
                    data = self.atomic_data[atom_clean]
                    self.add_log(f"\n⚛️ NUCLEAR INTERPRETATION:", 'cyan')
                    self.add_log(f"  Nucleus: {atom_clean}", 'white')
                    self.add_log(f"  Annealing simulated thermal equilibrium", 'white')
                    self.add_log(f"  Configuration represents {len(self.solution)} active orbitals", 'white')
                    
                    solution_mev = sum(self.solution) / 1000.0
                    self.add_log(f"  Solution binding: {solution_mev:.3f} MeV", 'white')
                    self.add_log(f"  Actual nucleus BE: {data['BE']:.3f} MeV", 'white')
                
                # Algorithm performance
                self.add_log(f"\n⚙️ ALGORITHM PERFORMANCE:", 'yellow')
                self.add_log(f"  Method: Simulated Annealing (Heuristic)", 'white')
                self.add_log(f"  Time elapsed: {elapsed:.3f} seconds", 'white')
                self.add_log(f"  Convergence: Probabilistic approximation", 'white')
                
                self.add_log(f"\n{'='*60}", 'white')
                
                self.status_label.config(text=f"Annealing solution: {len(self.solution)} orbitals")
            else:
                self.add_log(f"\n{'='*60}", 'white')
                self.add_log(f"✗ Annealing did not converge to exact solution", 'red')
                self.add_log(f"{'='*60}", 'white')
                self.add_log(f"\n⚠️ CONVERGENCE ANALYSIS:", 'yellow')
                self.add_log(f"  Best sum achieved: {sum(subset)} keV", 'white')
                self.add_log(f"  Target sum: {self.target} keV", 'white')
                self.add_log(f"  Error: {abs(sum(subset) - self.target)} keV", 'red')
                self.add_log(f"  Subset size: {len(subset)} orbitals", 'white')
                self.add_log(f"\n  Recommendations:", 'white')
                self.add_log(f"    • Try Exact DP method for guaranteed solution", 'white')
                self.add_log(f"    • Increase annealing iterations", 'white')
                self.add_log(f"    • Adjust temperature schedule", 'white')
                self.add_log(f"\n{'='*60}", 'white')
                self.status_label.config(text="Annealing failed to converge")
                
            self.running = False
            self.anneal_btn.config(state='normal')
            
        threading.Thread(target=run, daemon=True).start()
        
    def reset(self):
        self.numbers = []
        self.target = 0
        self.solution = None
        self.generated_subset = []
        self.data_text.delete(1.0, 'end')
        self.log_text.delete(1.0, 'end')
        self.canvas.delete('all')
        self.status_label.config(text="Ready to generate problem")
        self.add_log("System reset", 'yellow')

if __name__ == "__main__":
    root = tk.Tk()
    app = NuclearSSPSimulator(root)
    root.mainloop()
