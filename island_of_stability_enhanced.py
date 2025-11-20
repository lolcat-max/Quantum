import tkinter as tk
from tkinter import ttk, scrolledtext
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import cm
import numpy as np
import random
import threading
import time

class IslandOfStabilitySimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("⚛ Island of Stability - Nuclear Physics Simulator")
        self.root.geometry("1850x980")
        self.root.configure(bg='#0a0a1e')

        # Physics constants
        self.c = 299792458  # Speed of light (m/s)
        self.collision_count = 0
        self.running = False
        self.computing_islands = False

        # Island of stability data
        self.stability_islands = []
        self.all_predictions = []
        self.island_energies = {}

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
                'production_MeV': 342.052, 'formation': 'Silicon burning'
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

        # Extended magic numbers (including superheavy predictions)
        self.magic_numbers = {
            'proton': [2, 8, 20, 28, 50, 82, 114, 120, 126],  # 114, 120 are predicted
            'neutron': [2, 8, 20, 28, 50, 82, 126, 184, 228]  # 184, 228 are predicted superheavy
        }

        # Island search regions (Z_min, Z_max, N_min, N_max)
        self.search_regions = [
            (104, 120, 150, 190, "Superheavy Region 1"),
            (120, 140, 180, 230, "Superheavy Region 2"),
            (140, 160, 210, 260, "Hyperheavy Region"),
            (80, 90, 120, 140, "Actinide Extension"),
            (110, 118, 160, 180, "Island Core"),
        ]

        self.setup_ui()

        # Start precomputation after UI is ready
        self.root.after(500, self.precompute_all_islands)

    def setup_ui(self):
        """Setup the enhanced UI"""
        # Title
        title_frame = tk.Frame(self.root, bg='#0a0a1e')
        title_frame.pack(fill=tk.X, padx=10, pady=8)

        title = tk.Label(title_frame, text="⚛ ISLAND OF STABILITY - SUPERHEAVY ELEMENT PREDICTOR ⚛", 
                        font=('Arial', 19, 'bold'), fg='#00ffff', bg='#0a0a1e')
        title.pack()

        subtitle = tk.Label(title_frame, text="Dynamic Programming • Nuclear Shell Model • SEMF Predictions", 
                           font=('Arial', 10), fg='#00ff41', bg='#0a0a1e')
        subtitle.pack()

        # Main container
        main_container = tk.Frame(self.root, bg='#0a0a1e')
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Left panel - Controls (narrower)
        left_panel = tk.Frame(main_container, bg='#1a1a3e', relief=tk.RIDGE, bd=3, width=320)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
        left_panel.pack_propagate(False)

        tk.Label(left_panel, text="CONFIGURATION", 
                font=('Arial', 12, 'bold'), fg='#00ffff', bg='#1a1a3e').pack(pady=8)

        # Search region selector
        region_frame = tk.LabelFrame(left_panel, text="Search Region", 
                                    bg='#1a1a3e', fg='#00ff41', font=('Arial', 9, 'bold'))
        region_frame.pack(fill=tk.X, padx=8, pady=5)

        self.region_var = tk.StringVar(value="All Regions")
        region_options = ["All Regions"] + [r[4] for r in self.search_regions]
        region_menu = ttk.Combobox(region_frame, textvariable=self.region_var,
                                   values=region_options, state='readonly', width=22)
        region_menu.pack(pady=5, padx=5)

        # Target configuration
        target_frame = tk.LabelFrame(left_panel, text="Custom Target", 
                                    bg='#1a1a3e', fg='#00ff41', font=('Arial', 9, 'bold'))
        target_frame.pack(fill=tk.X, padx=8, pady=5)

        tk.Label(target_frame, text="Z (Protons):", fg='white', bg='#1a1a3e', 
                font=('Arial', 8)).pack(pady=(3,0))
        self.target_z_var = tk.StringVar(value="114")
        tk.Entry(target_frame, textvariable=self.target_z_var, width=12,
                bg='#0f0f2e', fg='white', font=('Arial', 9)).pack(pady=2)

        tk.Label(target_frame, text="N (Neutrons):", fg='white', bg='#1a1a3e',
                font=('Arial', 8)).pack()
        self.target_n_var = tk.StringVar(value="184")
        tk.Entry(target_frame, textvariable=self.target_n_var, width=12,
                bg='#0f0f2e', fg='white', font=('Arial', 9)).pack(pady=2)

        tk.Label(target_frame, text="Search Radius:", fg='white', bg='#1a1a3e',
                font=('Arial', 8)).pack()
        self.radius_var = tk.StringVar(value="15")
        tk.Entry(target_frame, textvariable=self.radius_var, width=12,
                bg='#0f0f2e', fg='white', font=('Arial', 9)).pack(pady=2)

        # Filters
        filter_frame = tk.LabelFrame(left_panel, text="Filters", 
                                    bg='#1a1a3e', fg='#00ff41', font=('Arial', 9, 'bold'))
        filter_frame.pack(fill=tk.X, padx=8, pady=5)

        self.show_magic_var = tk.BooleanVar(value=True)
        tk.Checkbutton(filter_frame, text="Magic Numbers Only", variable=self.show_magic_var,
                      bg='#1a1a3e', fg='white', selectcolor='#0f0f2e',
                      font=('Arial', 8)).pack(anchor=tk.W, padx=5, pady=2)

        self.show_doubly_var = tk.BooleanVar(value=True)
        tk.Checkbutton(filter_frame, text="Highlight Doubly Magic", variable=self.show_doubly_var,
                      bg='#1a1a3e', fg='white', selectcolor='#0f0f2e',
                      font=('Arial', 8)).pack(anchor=tk.W, padx=5, pady=2)

        tk.Label(filter_frame, text="Min BE/A (MeV):", fg='white', bg='#1a1a3e',
                font=('Arial', 8)).pack(pady=(3,0))
        self.min_be_var = tk.StringVar(value="7.0")
        tk.Entry(filter_frame, textvariable=self.min_be_var, width=12,
                bg='#0f0f2e', fg='white', font=('Arial', 9)).pack(pady=2)

        # Compute button
        self.compute_btn = tk.Button(left_panel, text="🔍 COMPUTE ISLANDS", 
                                    command=self.compute_islands_manual,
                                    bg='#00ff41', fg='black', font=('Arial', 10, 'bold'),
                                    width=22, height=2)
        self.compute_btn.pack(pady=10)

        self.update_btn = tk.Button(left_panel, text="🔄 UPDATE CHART", 
                                   command=self.update_all_plots,
                                   bg='#4444ff', fg='white', font=('Arial', 10, 'bold'),
                                   width=22)
        self.update_btn.pack(pady=5)

        # Progress
        self.progress_label = tk.Label(left_panel, text="Status: Ready", 
                                      fg='#00ffff', bg='#1a1a3e', font=('Arial', 9))
        self.progress_label.pack(pady=8)

        # Stats
        stats_frame = tk.LabelFrame(left_panel, text="Statistics", 
                                   bg='#1a1a3e', fg='#00ff41', font=('Arial', 9, 'bold'))
        stats_frame.pack(fill=tk.X, padx=8, pady=5)

        self.islands_label = tk.Label(stats_frame, text="Islands Found: 0", 
                                     fg='white', bg='#1a1a3e', font=('Arial', 8))
        self.islands_label.pack(anchor=tk.W, padx=5, pady=1)

        self.magic_label = tk.Label(stats_frame, text="Magic Nuclei: 0", 
                                   fg='white', bg='#1a1a3e', font=('Arial', 8))
        self.magic_label.pack(anchor=tk.W, padx=5, pady=1)

        self.doubly_label = tk.Label(stats_frame, text="Doubly Magic: 0", 
                                    fg='white', bg='#1a1a3e', font=('Arial', 8))
        self.doubly_label.pack(anchor=tk.W, padx=5, pady=1)

        self.max_be_label = tk.Label(stats_frame, text="Max BE/A: 0 MeV", 
                                    fg='white', bg='#1a1a3e', font=('Arial', 8))
        self.max_be_label.pack(anchor=tk.W, padx=5, pady=1)

        # Top predictions
        pred_frame = tk.LabelFrame(left_panel, text="Top Predictions", 
                                  bg='#1a1a3e', fg='#00ff41', font=('Arial', 9, 'bold'))
        pred_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=5)

        self.pred_text = scrolledtext.ScrolledText(pred_frame, height=12,
                                                   bg='#0f0f2e', fg='#00ff41',
                                                   font=('Courier', 7), wrap=tk.WORD)
        self.pred_text.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)

        # Right panel - Visualizations
        right_panel = tk.Frame(main_container, bg='#0a0a1e')
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Notebook for multiple charts
        notebook = ttk.Notebook(right_panel)
        notebook.pack(fill=tk.BOTH, expand=True)

        # Tab 1: Nuclear Chart
        chart_tab = tk.Frame(notebook, bg='#0f0f1e')
        notebook.add(chart_tab, text='🗺 Nuclear Chart')

        self.fig_chart = Figure(figsize=(13, 10), facecolor='#0f0f1e', dpi=100)
        self.canvas_chart = FigureCanvasTkAgg(self.fig_chart, master=chart_tab)
        self.canvas_chart.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Tab 2: 3D Landscape
        landscape_tab = tk.Frame(notebook, bg='#0f0f1e')
        notebook.add(landscape_tab, text='🏔 Energy Landscape')

        self.fig_3d = Figure(figsize=(13, 10), facecolor='#0f0f1e', dpi=100)
        self.canvas_3d = FigureCanvasTkAgg(self.fig_3d, master=landscape_tab)
        self.canvas_3d.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Tab 3: Heatmap
        heatmap_tab = tk.Frame(notebook, bg='#0f0f1e')
        notebook.add(heatmap_tab, text='🔥 Stability Heatmap')

        self.fig_heat = Figure(figsize=(13, 10), facecolor='#0f0f1e', dpi=100)
        self.canvas_heat = FigureCanvasTkAgg(self.fig_heat, master=heatmap_tab)
        self.canvas_heat.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Tab 4: Analysis
        analysis_tab = tk.Frame(notebook, bg='#0f0f1e')
        notebook.add(analysis_tab, text='📊 Analysis')

        self.fig_analysis = Figure(figsize=(13, 10), facecolor='#0f0f1e', dpi=100)
        self.canvas_analysis = FigureCanvasTkAgg(self.fig_analysis, master=analysis_tab)
        self.canvas_analysis.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Initialize empty plots
        self.init_all_plots()

    def init_all_plots(self):
        """Initialize all plot areas"""
        # Nuclear chart
        ax1 = self.fig_chart.add_subplot(111)
        ax1.set_facecolor('#0a0a1e')
        ax1.set_title('Initializing...', color='#00ffff', fontsize=14)
        ax1.tick_params(colors='white')
        self.fig_chart.tight_layout()
        self.canvas_chart.draw()

        # 3D landscape
        ax2 = self.fig_3d.add_subplot(111, projection='3d')
        ax2.set_facecolor('#0a0a1e')
        ax2.set_title('Initializing...', color='#00ffff', fontsize=14)
        self.fig_3d.tight_layout()
        self.canvas_3d.draw()

        # Heatmap
        ax3 = self.fig_heat.add_subplot(111)
        ax3.set_facecolor('#0a0a1e')
        ax3.set_title('Initializing...', color='#00ffff', fontsize=14)
        self.fig_heat.tight_layout()
        self.canvas_heat.draw()

        # Analysis
        ax4 = self.fig_analysis.add_subplot(111)
        ax4.set_facecolor('#0a0a1e')
        ax4.set_title('Initializing...', color='#00ffff', fontsize=14)
        self.fig_analysis.tight_layout()
        self.canvas_analysis.draw()

    def precompute_all_islands(self):
        """Precompute islands across all regions"""
        if self.computing_islands:
            return

        self.progress_label.config(text="Status: Precomputing islands...")
        self.computing_islands = True
        self.compute_btn.config(state=tk.DISABLED)

        threading.Thread(target=self._compute_all_islands_thread, daemon=True).start()

    def compute_islands_manual(self):
        """Manually trigger computation"""
        self.precompute_all_islands()

    def _compute_all_islands_thread(self):
        """Background thread for comprehensive island computation"""
        self.all_predictions = []
        self.stability_islands = []

        # Get known stable isotopes
        stable_isotopes = []
        for name, data in self.atomic_data.items():
            if 'stable' in data.get('stability', '').lower():
                stable_isotopes.append({
                    'name': name,
                    'Z': data['Z'],
                    'N': data['N'],
                    'A': data['Z'] + data['N'],
                    'BE': data['BE'],
                    'BE_per_A': data['BE_per_A']
                })

        total_predictions = 0

        # Search all regions
        for z_min, z_max, n_min, n_max, region_name in self.search_regions:
            self.root.after(0, lambda r=region_name: self.progress_label.config(
                text=f"Scanning: {r}..."))

            # Fine-grained search with step=2
            for z in range(z_min, z_max + 1, 2):
                for n in range(n_min, n_max + 1, 2):
                    island = self.calculate_stability(z, n, stable_isotopes)
                    if island:
                        self.all_predictions.append(island)
                        total_predictions += 1

                        # High-quality predictions
                        if island['BE_per_A'] > 7.0 or island['magic'] or island['doubly_magic']:
                            self.stability_islands.append(island)

        # Search around custom target with finer resolution
        try:
            target_z = int(self.target_z_var.get())
            target_n = int(self.target_n_var.get())
            radius = int(self.radius_var.get())

            for dz in range(-radius, radius + 1):
                for dn in range(-radius, radius + 1):
                    z = target_z + dz
                    n = target_n + dn
                    if z > 0 and n > 0:
                        island = self.calculate_stability(z, n, stable_isotopes)
                        if island and island not in self.all_predictions:
                            self.all_predictions.append(island)
                            if island['BE_per_A'] > 7.0 or island['magic']:
                                self.stability_islands.append(island)
        except:
            pass

        # Remove duplicates
        seen = set()
        unique_islands = []
        for island in self.stability_islands:
            key = (island['Z'], island['N'])
            if key not in seen:
                seen.add(key)
                unique_islands.append(island)

        self.stability_islands = unique_islands

        # Update UI
        self.root.after(0, self.update_statistics)
        self.root.after(0, self.update_predictions_list)
        self.root.after(0, self.update_all_plots)

        self.computing_islands = False
        self.root.after(0, lambda: self.progress_label.config(
            text=f"Complete: {len(self.stability_islands)} islands found!"))
        self.root.after(0, lambda: self.compute_btn.config(state=tk.NORMAL))

    def calculate_stability(self, z, n, known_isotopes):
        """Calculate nuclear stability using SEMF + shell model"""
        A = z + n
        if A <= 0:
            return None

        # Semi-Empirical Mass Formula (SEMF) - Improved coefficients
        a_v = 15.75   # Volume
        a_s = 17.8    # Surface
        a_c = 0.711   # Coulomb
        a_a = 23.7    # Asymmetry
        a_p = 11.18   # Pairing

        volume = a_v * A
        surface = -a_s * (A ** (2/3))
        coulomb = -a_c * (z ** 2) / (A ** (1/3))
        asymmetry = -a_a * ((n - z) ** 2) / A

        # Pairing term
        if z % 2 == 0 and n % 2 == 0:
            pairing = a_p / (A ** 0.5)
        elif z % 2 == 1 and n % 2 == 1:
            pairing = -a_p / (A ** 0.5)
        else:
            pairing = 0

        BE = volume + surface + coulomb + asymmetry + pairing
        BE_per_A = BE / A

        # Shell corrections (magic number bonus)
        shell_bonus = 0.0
        z_magic = z in self.magic_numbers['proton']
        n_magic = n in self.magic_numbers['neutron']

        if z_magic:
            shell_bonus += 2.5
        if n_magic:
            shell_bonus += 2.5
        if z_magic and n_magic:
            shell_bonus += 4.0  # Extra bonus for doubly magic

        # Distance from nearest magic number (closer is better)
        z_dist = min(abs(z - m) for m in self.magic_numbers['proton'])
        n_dist = min(abs(n - m) for m in self.magic_numbers['neutron'])

        if z_dist <= 2:
            shell_bonus += 0.5
        if n_dist <= 2:
            shell_bonus += 0.5

        BE_per_A += shell_bonus

        # Stability score (higher is better)
        stability_score = BE_per_A
        if z_magic or n_magic:
            stability_score += 2.0
        if z_magic and n_magic:
            stability_score += 5.0

        return {
            'Z': z,
            'N': n,
            'A': A,
            'BE': BE,
            'BE_per_A': BE_per_A,
            'shell_bonus': shell_bonus,
            'magic': z_magic or n_magic,
            'doubly_magic': z_magic and n_magic,
            'z_magic': z_magic,
            'n_magic': n_magic,
            'stability_score': stability_score,
            'z_dist_magic': z_dist,
            'n_dist_magic': n_dist
        }

    def update_statistics(self):
        """Update statistics display"""
        total = len(self.stability_islands)
        magic = sum(1 for i in self.stability_islands if i['magic'])
        doubly = sum(1 for i in self.stability_islands if i['doubly_magic'])
        max_be = max((i['BE_per_A'] for i in self.stability_islands), default=0)

        self.islands_label.config(text=f"Islands Found: {total}")
        self.magic_label.config(text=f"Magic Nuclei: {magic}")
        self.doubly_label.config(text=f"Doubly Magic: {doubly}")
        self.max_be_label.config(text=f"Max BE/A: {max_be:.3f} MeV")

    def update_predictions_list(self):
        """Update top predictions text"""
        self.pred_text.delete(1.0, tk.END)

        if not self.stability_islands:
            self.pred_text.insert(tk.END, "No predictions yet.\n")
            return

        # Sort by stability score
        sorted_islands = sorted(self.stability_islands, 
                               key=lambda x: x['stability_score'], reverse=True)

        self.pred_text.insert(tk.END, f"TOP {min(25, len(sorted_islands))} PREDICTIONS\n")
        self.pred_text.insert(tk.END, "=" * 38 + "\n\n")

        for i, island in enumerate(sorted_islands[:25], 1):
            magic_str = ""
            if island['doubly_magic']:
                magic_str = " ⚛⚛"
            elif island['magic']:
                magic_str = " ⚛"

            self.pred_text.insert(tk.END, 
                f"{i:2d}. Z={island['Z']:3d} N={island['N']:3d}{magic_str}\n")
            self.pred_text.insert(tk.END, 
                f"    BE/A={island['BE_per_A']:6.3f} MeV\n")
            self.pred_text.insert(tk.END, 
                f"    Score={island['stability_score']:5.2f}\n\n")

    def update_all_plots(self):
        """Update all visualization plots"""
        self.plot_nuclear_chart()
        self.plot_3d_landscape()
        self.plot_heatmap()
        self.plot_analysis()

    def plot_nuclear_chart(self):
        """Plot enhanced nuclear chart"""
        self.fig_chart.clear()
        ax = self.fig_chart.add_subplot(111)
        ax.set_facecolor('#0a0a1e')
        ax.set_title('Nuclear Chart - Islands of Stability', 
                    color='#00ffff', fontsize=15, fontweight='bold', pad=15)
        ax.set_xlabel('Neutron Number (N)', color='white', fontsize=12, fontweight='bold')
        ax.set_ylabel('Proton Number (Z)', color='white', fontsize=12, fontweight='bold')
        ax.tick_params(colors='white', labelsize=9)
        for spine in ax.spines.values():
            spine.set_color('white')
        ax.grid(True, alpha=0.15, color='cyan', linestyle=':', linewidth=0.5)

        # Plot known stable isotopes (smaller)
        known_z, known_n, known_be = [], [], []
        for name, data in self.atomic_data.items():
            if 'stable' in data.get('stability', '').lower():
                known_z.append(data['Z'])
                known_n.append(data['N'])
                known_be.append(data['BE_per_A'])

        if known_z:
            ax.scatter(known_n, known_z, s=50, c=known_be, cmap='viridis',
                      edgecolors='white', linewidths=0.8, alpha=0.6, 
                      label='Known Stable', zorder=2)

        # Plot predicted islands
        if self.stability_islands:
            # Regular islands
            regular = [i for i in self.stability_islands if not i['doubly_magic']]
            if regular:
                r_z = [i['Z'] for i in regular]
                r_n = [i['N'] for i in regular]
                r_be = [i['BE_per_A'] for i in regular]
                scatter = ax.scatter(r_n, r_z, s=180, c=r_be, cmap='plasma',
                                   edgecolors='cyan', linewidths=2, alpha=0.9,
                                   marker='*', label='Predicted Islands', zorder=3)

            # Doubly magic (extra highlight)
            doubly = [i for i in self.stability_islands if i['doubly_magic']]
            if doubly:
                d_z = [i['Z'] for i in doubly]
                d_n = [i['N'] for i in doubly]
                d_be = [i['BE_per_A'] for i in doubly]
                ax.scatter(d_n, d_z, s=350, c=d_be, cmap='hot',
                          edgecolors='red', linewidths=3.5, alpha=1.0,
                          marker='*', label='Doubly Magic', zorder=4)

                # Add labels for doubly magic
                for i in doubly:
                    ax.annotate(f"{i['Z']},{i['N']}", 
                               xy=(i['N'], i['Z']), xytext=(5, 5),
                               textcoords='offset points', color='yellow',
                               fontsize=8, fontweight='bold')

            # Add colorbar
            if regular:
                cbar = self.fig_chart.colorbar(scatter, ax=ax, pad=0.02)
                cbar.set_label('BE/A (MeV)', color='white', fontsize=10, fontweight='bold')
                cbar.ax.yaxis.set_tick_params(color='white', labelcolor='white', labelsize=8)

        # Draw magic number lines
        for magic_z in self.magic_numbers['proton']:
            if magic_z <= 150:
                ax.axhline(y=magic_z, color='yellow', linestyle='--', 
                          linewidth=1, alpha=0.25, zorder=1)
        for magic_n in self.magic_numbers['neutron']:
            if magic_n <= 250:
                ax.axvline(x=magic_n, color='yellow', linestyle='--', 
                          linewidth=1, alpha=0.25, zorder=1)

        # Add N=Z line
        max_val = 160
        ax.plot([0, max_val], [0, max_val], 'r--', linewidth=1.5, 
               alpha=0.4, label='N=Z', zorder=1)

        ax.legend(facecolor='#1a1a3e', edgecolor='cyan', labelcolor='white',
                 fontsize=9, loc='upper left')

        # Set reasonable axis limits
        if self.stability_islands:
            all_n = [i['N'] for i in self.stability_islands] + known_n
            all_z = [i['Z'] for i in self.stability_islands] + known_z
            ax.set_xlim(min(all_n) - 10, max(all_n) + 10)
            ax.set_ylim(min(all_z) - 5, max(all_z) + 5)

        self.fig_chart.tight_layout()
        self.canvas_chart.draw()

    def plot_3d_landscape(self):
        """Plot 3D binding energy landscape"""
        self.fig_3d.clear()
        ax = self.fig_3d.add_subplot(111, projection='3d')
        ax.set_facecolor('#0a0a1e')
        ax.set_title('Binding Energy Landscape', 
                    color='#00ffff', fontsize=15, fontweight='bold', pad=15)
        ax.set_xlabel('N', color='white', fontsize=11, fontweight='bold')
        ax.set_ylabel('Z', color='white', fontsize=11, fontweight='bold')
        ax.set_zlabel('BE/A (MeV)', color='white', fontsize=11, fontweight='bold')
        ax.tick_params(colors='white', labelsize=8)
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        ax.grid(True, alpha=0.2, color='cyan', linestyle=':')

        # Known isotopes
        known_n, known_z, known_be = [], [], []
        for name, data in self.atomic_data.items():
            if 'stable' in data.get('stability', '').lower():
                known_n.append(data['N'])
                known_z.append(data['Z'])
                known_be.append(data['BE_per_A'])

        if known_n:
            ax.scatter(known_n, known_z, known_be, s=40, c=known_be,
                      cmap='viridis', alpha=0.6, edgecolors='white', linewidths=0.5)

        # Predicted islands
        if self.stability_islands:
            island_n = [i['N'] for i in self.stability_islands]
            island_z = [i['Z'] for i in self.stability_islands]
            island_be = [i['BE_per_A'] for i in self.stability_islands]

            scatter = ax.scatter(island_n, island_z, island_be, s=150, c=island_be,
                               cmap='plasma', alpha=0.9, edgecolors='cyan', 
                               linewidths=2, marker='*', depthshade=True)

            cbar = self.fig_3d.colorbar(scatter, ax=ax, pad=0.1, shrink=0.7)
            cbar.set_label('BE/A (MeV)', color='white', fontsize=10, fontweight='bold')
            cbar.ax.yaxis.set_tick_params(color='white', labelcolor='white', labelsize=8)

        ax.view_init(elev=25, azim=45)

        self.fig_3d.tight_layout()
        self.canvas_3d.draw()

    def plot_heatmap(self):
        """Plot stability heatmap"""
        self.fig_heat.clear()
        ax = self.fig_heat.add_subplot(111)
        ax.set_facecolor('#0a0a1e')
        ax.set_title('Nuclear Stability Heatmap', 
                    color='#00ffff', fontsize=15, fontweight='bold', pad=15)
        ax.set_xlabel('Neutron Number (N)', color='white', fontsize=12, fontweight='bold')
        ax.set_ylabel('Proton Number (Z)', color='white', fontsize=12, fontweight='bold')
        ax.tick_params(colors='white', labelsize=9)
        for spine in ax.spines.values():
            spine.set_color('white')

        if not self.all_predictions:
            ax.text(0.5, 0.5, 'Computing...', transform=ax.transAxes,
                   ha='center', va='center', color='white', fontsize=14)
            self.fig_heat.tight_layout()
            self.canvas_heat.draw()
            return

        # Create grid
        all_z = [p['Z'] for p in self.all_predictions]
        all_n = [p['N'] for p in self.all_predictions]
        all_be = [p['BE_per_A'] for p in self.all_predictions]

        z_min, z_max = min(all_z), max(all_z)
        n_min, n_max = min(all_n), max(all_n)

        # Create heatmap grid
        grid_z = np.arange(z_min, z_max + 1)
        grid_n = np.arange(n_min, n_max + 1)
        heatmap = np.zeros((len(grid_z), len(grid_n)))

        for p in self.all_predictions:
            z_idx = p['Z'] - z_min
            n_idx = p['N'] - n_min
            if 0 <= z_idx < len(grid_z) and 0 <= n_idx < len(grid_n):
                heatmap[z_idx, n_idx] = p['BE_per_A']

        # Plot heatmap
        im = ax.imshow(heatmap, cmap='hot', aspect='auto', origin='lower',
                      extent=[n_min, n_max, z_min, z_max], interpolation='bilinear')

        cbar = self.fig_heat.colorbar(im, ax=ax, pad=0.02)
        cbar.set_label('BE/A (MeV)', color='white', fontsize=10, fontweight='bold')
        cbar.ax.yaxis.set_tick_params(color='white', labelcolor='white', labelsize=8)

        # Overlay magic number lines
        for magic_z in self.magic_numbers['proton']:
            if z_min <= magic_z <= z_max:
                ax.axhline(y=magic_z, color='cyan', linestyle='--', 
                          linewidth=1.5, alpha=0.6)
        for magic_n in self.magic_numbers['neutron']:
            if n_min <= magic_n <= n_max:
                ax.axvline(x=magic_n, color='cyan', linestyle='--', 
                          linewidth=1.5, alpha=0.6)

        self.fig_heat.tight_layout()
        self.canvas_heat.draw()

    def plot_analysis(self):
        """Plot statistical analysis"""
        self.fig_analysis.clear()

        if not self.stability_islands:
            ax = self.fig_analysis.add_subplot(111)
            ax.set_facecolor('#0a0a1e')
            ax.text(0.5, 0.5, 'No data yet', transform=ax.transAxes,
                   ha='center', va='center', color='white', fontsize=14)
            self.fig_analysis.tight_layout()
            self.canvas_analysis.draw()
            return

        # 2x2 subplot grid
        # 1. BE/A distribution
        ax1 = self.fig_analysis.add_subplot(2, 2, 1)
        ax1.set_facecolor('#0a0a1e')
        ax1.set_title('BE/A Distribution', color='cyan', fontsize=11, fontweight='bold')
        be_values = [i['BE_per_A'] for i in self.stability_islands]
        ax1.hist(be_values, bins=25, color='cyan', alpha=0.7, edgecolor='white', linewidth=1)
        ax1.set_xlabel('BE/A (MeV)', color='white', fontsize=9)
        ax1.set_ylabel('Count', color='white', fontsize=9)
        ax1.tick_params(colors='white', labelsize=8)
        ax1.grid(True, alpha=0.2, color='white', linestyle=':')
        for spine in ax1.spines.values():
            spine.set_color('white')

        # 2. N/Z ratio
        ax2 = self.fig_analysis.add_subplot(2, 2, 2)
        ax2.set_facecolor('#0a0a1e')
        ax2.set_title('N/Z Ratio vs Mass', color='cyan', fontsize=11, fontweight='bold')
        a_values = [i['A'] for i in self.stability_islands]
        nz_values = [i['N']/i['Z'] for i in self.stability_islands]
        be_colors = [i['BE_per_A'] for i in self.stability_islands]
        scatter = ax2.scatter(a_values, nz_values, s=80, c=be_colors, cmap='plasma',
                            edgecolors='white', linewidths=1, alpha=0.8)
        ax2.set_xlabel('Mass Number (A)', color='white', fontsize=9)
        ax2.set_ylabel('N/Z Ratio', color='white', fontsize=9)
        ax2.axhline(y=1, color='red', linestyle='--', linewidth=1, alpha=0.5)
        ax2.tick_params(colors='white', labelsize=8)
        ax2.grid(True, alpha=0.2, color='white', linestyle=':')
        for spine in ax2.spines.values():
            spine.set_color('white')

        # 3. Shell bonus distribution
        ax3 = self.fig_analysis.add_subplot(2, 2, 3)
        ax3.set_facecolor('#0a0a1e')
        ax3.set_title('Shell Bonus Effect', color='cyan', fontsize=11, fontweight='bold')
        bonus_values = [i['shell_bonus'] for i in self.stability_islands]
        ax3.hist(bonus_values, bins=15, color='lime', alpha=0.7, edgecolor='white', linewidth=1)
        ax3.set_xlabel('Shell Bonus (MeV)', color='white', fontsize=9)
        ax3.set_ylabel('Count', color='white', fontsize=9)
        ax3.tick_params(colors='white', labelsize=8)
        ax3.grid(True, alpha=0.2, color='white', linestyle=':')
        for spine in ax3.spines.values():
            spine.set_color('white')

        # 4. Magic number proximity
        ax4 = self.fig_analysis.add_subplot(2, 2, 4)
        ax4.set_facecolor('#0a0a1e')
        ax4.set_title('Nuclei by Magic Status', color='cyan', fontsize=11, fontweight='bold')

        doubly_count = sum(1 for i in self.stability_islands if i['doubly_magic'])
        magic_count = sum(1 for i in self.stability_islands if i['magic'] and not i['doubly_magic'])
        normal_count = len(self.stability_islands) - doubly_count - magic_count

        categories = ['Doubly\nMagic', 'Magic', 'Normal']
        counts = [doubly_count, magic_count, normal_count]
        colors_bar = ['#ff4444', '#ffaa00', '#4444ff']

        bars = ax4.bar(categories, counts, color=colors_bar, edgecolor='white', linewidth=2, alpha=0.8)
        ax4.set_ylabel('Count', color='white', fontsize=9)
        ax4.tick_params(colors='white', labelsize=8)
        ax4.grid(True, alpha=0.2, color='white', linestyle=':', axis='y')
        for spine in ax4.spines.values():
            spine.set_color('white')

        # Add count labels on bars
        for bar, count in zip(bars, counts):
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height,
                    f'{count}', ha='center', va='bottom', 
                    color='white', fontsize=10, fontweight='bold')

        self.fig_analysis.tight_layout()
        self.canvas_analysis.draw()

def main():
    root = tk.Tk()
    app = IslandOfStabilitySimulator(root)
    root.mainloop()

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    main()
