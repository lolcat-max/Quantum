import tkinter as tk
from tkinter import ttk, scrolledtext
import random
import threading
import time
import math
from collections import defaultdict

class NuclearSSPSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("SSP Quantum Chemistry Simulator - EXTENSIVE DATABASE")
        self.root.geometry("1750x1000")
        self.root.configure(bg='#0f172a') 

        self.numbers = []
        self.number_labels = []
        self.target = 0
        self.solution = None
        self.solution_path = []
        self.running = False

        self.shell_names = ['1s', '2s/2p', '3s/3p', '4s/3d/4p', '5s/4d/5p', '6s/4f/5d/6p']

        # --- EXTENSIVE ATOMIC DATA (Periods 1-4 + Key Metals) ---
        self.atomic_data = {
            # Period 1
            'Hydrogen (H-1)': {'Z': 1, 'shells': [1], 'symbol': 'H'},
            'Helium (He-4)': {'Z': 2, 'shells': [2], 'symbol': 'He'},
            # Period 2
            'Lithium (Li-7)': {'Z': 3, 'shells': [2, 1], 'symbol': 'Li'},
            'Beryllium (Be-9)': {'Z': 4, 'shells': [2, 2], 'symbol': 'Be'},
            'Boron (B-11)': {'Z': 5, 'shells': [2, 3], 'symbol': 'B'},
            'Carbon (C-12)': {'Z': 6, 'shells': [2, 4], 'symbol': 'C'},
            'Nitrogen (N-14)': {'Z': 7, 'shells': [2, 5], 'symbol': 'N'},
            'Oxygen (O-16)': {'Z': 8, 'shells': [2, 6], 'symbol': 'O'},
            'Fluorine (F-19)': {'Z': 9, 'shells': [2, 7], 'symbol': 'F'},
            'Neon (Ne-20)': {'Z': 10, 'shells': [2, 8], 'symbol': 'Ne'},
            # Period 3
            'Sodium (Na-23)': {'Z': 11, 'shells': [2, 8, 1], 'symbol': 'Na'},
            'Magnesium (Mg-24)': {'Z': 12, 'shells': [2, 8, 2], 'symbol': 'Mg'},
            'Aluminum (Al-27)': {'Z': 13, 'shells': [2, 8, 3], 'symbol': 'Al'},
            'Silicon (Si-28)': {'Z': 14, 'shells': [2, 8, 4], 'symbol': 'Si'},
            'Phosphorus (P-31)': {'Z': 15, 'shells': [2, 8, 5], 'symbol': 'P'},
            'Sulfur (S-32)': {'Z': 16, 'shells': [2, 8, 6], 'symbol': 'S'},
            'Chlorine (Cl-35)': {'Z': 17, 'shells': [2, 8, 7], 'symbol': 'Cl'},
            'Argon (Ar-40)': {'Z': 18, 'shells': [2, 8, 8], 'symbol': 'Ar'},
            # Period 4 (Key Elements)
            'Potassium (K-39)': {'Z': 19, 'shells': [2, 8, 8, 1], 'symbol': 'K'},
            'Calcium (Ca-40)': {'Z': 20, 'shells': [2, 8, 8, 2], 'symbol': 'Ca'},
            'Titanium (Ti-48)': {'Z': 22, 'shells': [2, 8, 10, 2], 'symbol': 'Ti'},
            'Iron (Fe-56)': {'Z': 26, 'shells': [2, 8, 14, 2], 'symbol': 'Fe'},
            'Cobalt (Co-59)': {'Z': 27, 'shells': [2, 8, 15, 2], 'symbol': 'Co'},
            'Nickel (Ni-58)': {'Z': 28, 'shells': [2, 8, 16, 2], 'symbol': 'Ni'},
            'Copper (Cu-63)': {'Z': 29, 'shells': [2, 8, 18, 1], 'symbol': 'Cu'},
            'Zinc (Zn-64)': {'Z': 30, 'shells': [2, 8, 18, 2], 'symbol': 'Zn'},
            'Bromine (Br-79)': {'Z': 35, 'shells': [2, 8, 18, 7], 'symbol': 'Br'},
            # Heavy Metals
            'Silver (Ag-107)': {'Z': 47, 'shells': [2, 8, 18, 18, 1], 'symbol': 'Ag'},
            'Gold (Au-197)': {'Z': 79, 'shells': [2, 8, 18, 32, 18, 1], 'symbol': 'Au'},
            'Lead (Pb-208)': {'Z': 82, 'shells': [2, 8, 18, 32, 18, 4], 'symbol': 'Pb'},
        }

        # --- EXTENSIVE MOLECULAR DATABASE ---
        self.molecular_data = {
            # --- INORGANIC SALTS ---
            'Table Salt (NaCl)': {'formula': 'NaCl', 'atoms': [('Sodium (Na-23)', 1), ('Chlorine (Cl-35)', 1)]},
            'Potassium Chloride (KCl)': {'formula': 'KCl', 'atoms': [('Potassium (K-39)', 1), ('Chlorine (Cl-35)', 1)]},
            'Calcium Carbonate (CaCO3)': {'formula': 'CaCO3', 'atoms': [('Calcium (Ca-40)', 1), ('Carbon (C-12)', 1), ('Oxygen (O-16)', 3)]},
            'Magnesium Sulfate (MgSO4)': {'formula': 'MgSO4', 'atoms': [('Magnesium (Mg-24)', 1), ('Sulfur (S-32)', 1), ('Oxygen (O-16)', 4)]},
            'Copper Sulfate (CuSO4)': {'formula': 'CuSO4', 'atoms': [('Copper (Cu-63)', 1), ('Sulfur (S-32)', 1), ('Oxygen (O-16)', 4)]},
            'Sodium Bicarbonate (NaHCO3)': {'formula': 'NaHCO3', 'atoms': [('Sodium (Na-23)', 1), ('Hydrogen (H-1)', 1), ('Carbon (C-12)', 1), ('Oxygen (O-16)', 3)]},
            'Silver Nitrate (AgNO3)': {'formula': 'AgNO3', 'atoms': [('Silver (Ag-107)', 1), ('Nitrogen (N-14)', 1), ('Oxygen (O-16)', 3)]},

            # --- ACIDS & BASES ---
            'Hydrochloric Acid (HCl)': {'formula': 'HCl', 'atoms': [('Hydrogen (H-1)', 1), ('Chlorine (Cl-35)', 1)]},
            'Sulfuric Acid (H2SO4)': {'formula': 'H2SO4', 'atoms': [('Hydrogen (H-1)', 2), ('Sulfur (S-32)', 1), ('Oxygen (O-16)', 4)]},
            'Nitric Acid (HNO3)': {'formula': 'HNO3', 'atoms': [('Hydrogen (H-1)', 1), ('Nitrogen (N-14)', 1), ('Oxygen (O-16)', 3)]},
            'Phosphoric Acid (H3PO4)': {'formula': 'H3PO4', 'atoms': [('Hydrogen (H-1)', 3), ('Phosphorus (P-31)', 1), ('Oxygen (O-16)', 4)]},
            'Sodium Hydroxide (NaOH)': {'formula': 'NaOH', 'atoms': [('Sodium (Na-23)', 1), ('Oxygen (O-16)', 1), ('Hydrogen (H-1)', 1)]},
            'Ammonia (NH3)': {'formula': 'NH3', 'atoms': [('Nitrogen (N-14)', 1), ('Hydrogen (H-1)', 3)]},

            # --- HYDROCARBONS (Alkanes) ---
            'Methane (CH4)': {'formula': 'CH4', 'atoms': [('Carbon (C-12)', 1), ('Hydrogen (H-1)', 4)]},
            'Ethane (C2H6)': {'formula': 'C2H6', 'atoms': [('Carbon (C-12)', 2), ('Hydrogen (H-1)', 6)]},
            'Propane (C3H8)': {'formula': 'C3H8', 'atoms': [('Carbon (C-12)', 3), ('Hydrogen (H-1)', 8)]},
            'Butane (C4H10)': {'formula': 'C4H10', 'atoms': [('Carbon (C-12)', 4), ('Hydrogen (H-1)', 10)]},
            'Pentane (C5H12)': {'formula': 'C5H12', 'atoms': [('Carbon (C-12)', 5), ('Hydrogen (H-1)', 12)]},
            'Hexane (C6H14)': {'formula': 'C6H14', 'atoms': [('Carbon (C-12)', 6), ('Hydrogen (H-1)', 14)]},
            'Octane (C8H18)': {'formula': 'C8H18', 'atoms': [('Carbon (C-12)', 8), ('Hydrogen (H-1)', 18)]},

            # --- ALCOHOLS & SOLVENTS ---
            'Methanol (CH3OH)': {'formula': 'CH3OH', 'atoms': [('Carbon (C-12)', 1), ('Hydrogen (H-1)', 4), ('Oxygen (O-16)', 1)]},
            'Ethanol (C2H5OH)': {'formula': 'C2H5OH', 'atoms': [('Carbon (C-12)', 2), ('Hydrogen (H-1)', 6), ('Oxygen (O-16)', 1)]},
            'Isopropanol (C3H8O)': {'formula': 'C3H8O', 'atoms': [('Carbon (C-12)', 3), ('Hydrogen (H-1)', 8), ('Oxygen (O-16)', 1)]},
            'Acetone (C3H6O)': {'formula': 'C3H6O', 'atoms': [('Carbon (C-12)', 3), ('Hydrogen (H-1)', 6), ('Oxygen (O-16)', 1)]},
            'Benzene (C6H6)': {'formula': 'C6H6', 'atoms': [('Carbon (C-12)', 6), ('Hydrogen (H-1)', 6)]},
            'Toluene (C7H8)': {'formula': 'C7H8', 'atoms': [('Carbon (C-12)', 7), ('Hydrogen (H-1)', 8)]},

            # --- BIOCHEMISTRY ---
            'Glucose (C6H12O6)': {'formula': 'C6H12O6', 'atoms': [('Carbon (C-12)', 6), ('Hydrogen (H-1)', 12), ('Oxygen (O-16)', 6)]},
            'Sucrose (C12H22O11)': {'formula': 'C12H22O11', 'atoms': [('Carbon (C-12)', 12), ('Hydrogen (H-1)', 22), ('Oxygen (O-16)', 11)]},
            'Glycine (C2H5NO2)': {'formula': 'C2H5NO2', 'atoms': [('Carbon (C-12)', 2), ('Hydrogen (H-1)', 5), ('Nitrogen (N-14)', 1), ('Oxygen (O-16)', 2)]},
            'Urea (CH4N2O)': {'formula': 'CH4N2O', 'atoms': [('Carbon (C-12)', 1), ('Hydrogen (H-1)', 4), ('Nitrogen (N-14)', 2), ('Oxygen (O-16)', 1)]},
            'Caffeine (C8H10N4O2)': {'formula': 'C8H10N4O2', 'atoms': [('Carbon (C-12)', 8), ('Hydrogen (H-1)', 10), ('Nitrogen (N-14)', 4), ('Oxygen (O-16)', 2)]},
            'Aspirin (C9H8O4)': {'formula': 'C9H8O4', 'atoms': [('Carbon (C-12)', 9), ('Hydrogen (H-1)', 8), ('Oxygen (O-16)', 4)]},

            # --- MATERIALS ---
            'Water (H2O)': {'formula': 'H2O', 'atoms': [('Hydrogen (H-1)', 2), ('Oxygen (O-16)', 1)]},
            'Sand (SiO2)': {'formula': 'SiO2', 'atoms': [('Silicon (Si-28)', 1), ('Oxygen (O-16)', 2)]},
            'Rust (Fe2O3)': {'formula': 'Fe2O3', 'atoms': [('Iron (Fe-56)', 2), ('Oxygen (O-16)', 3)]},
            'Titanium Dioxide (TiO2)': {'formula': 'TiO2', 'atoms': [('Titanium (Ti-48)', 1), ('Oxygen (O-16)', 2)]},
        }

        self.setup_ui()

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TCombobox', fieldbackground='#334155', background='#1e293b', foreground='white')

        header = tk.Frame(self.root, bg='#1e293b', height=60)
        header.pack(fill='x')
        tk.Label(header, text="⚛ QUANTUM SYNTHESIS STUDIO - EXTENSIVE DB", 
                font=('Segoe UI', 20, 'bold'), bg='#1e293b', fg='#38bdf8').pack(pady=10)

        controls = tk.Frame(self.root, bg='#334155', padx=10, pady=10)
        controls.pack(fill='x', padx=10, pady=10)

        tk.Label(controls, text="Target System:", bg='#334155', fg='white').pack(side='left', padx=5)
        self.atom_var = tk.StringVar(value="Methanol (CH3OH)")
        self.atom_dropdown = ttk.Combobox(controls, textvariable=self.atom_var, width=45, state='readonly')

        # Categories for dropdown
        cats = [
            '--- HYDROCARBONS ---', 'Methane (CH4)', 'Ethane (C2H6)', 'Propane (C3H8)', 'Butane (C4H10)', 'Octane (C8H18)',
            '--- ALCOHOLS & SOLVENTS ---', 'Methanol (CH3OH)', 'Ethanol (C2H5OH)', 'Isopropanol (C3H8O)', 'Acetone (C3H6O)',
            '--- ACIDS & BASES ---', 'Hydrochloric Acid (HCl)', 'Sulfuric Acid (H2SO4)', 'Sodium Hydroxide (NaOH)', 'Ammonia (NH3)',
            '--- INORGANIC SALTS ---', 'Table Salt (NaCl)', 'Calcium Carbonate (CaCO3)', 'Copper Sulfate (CuSO4)',
            '--- BIOCHEMISTRY ---', 'Glucose (C6H12O6)', 'Caffeine (C8H10N4O2)', 'Aspirin (C9H8O4)', 'Glycine (C2H5NO2)',
            '--- MATERIALS ---', 'Sand (SiO2)', 'Rust (Fe2O3)', 'Titanium Dioxide (TiO2)',
            '--- ATOMS (METALS) ---', 'Iron (Fe-56)', 'Copper (Cu-63)', 'Gold (Au-197)', 'Silver (Ag-107)'
        ]

        self.atom_dropdown['values'] = cats
        self.atom_dropdown.pack(side='left', padx=5)
        self.atom_dropdown.bind('<<ComboboxSelected>>', self.on_system_select)

        tk.Button(controls, text="1. Initialize System", command=self.generate_problem,
                 bg='#10b981', fg='white', font=('Segoe UI', 10, 'bold')).pack(side='left', padx=10)

        tk.Button(controls, text="2. Run Full Analysis", command=self.solve_full_analysis,
                 bg='#3b82f6', fg='white', font=('Segoe UI', 10, 'bold')).pack(side='left', padx=5)

        tk.Button(controls, text="Reset", command=self.reset,
                 bg='#64748b', fg='white').pack(side='right', padx=10)

        workspace = tk.PanedWindow(self.root, orient='horizontal', bg='#0f172a')
        workspace.pack(fill='both', expand=True, padx=10, pady=5)

        frame_data = tk.LabelFrame(workspace, text="System Specifications", bg='#1e293b', fg='#94a3b8', font=('Segoe UI', 11))
        workspace.add(frame_data, width=400)

        self.data_text = scrolledtext.ScrolledText(frame_data, bg='#0f172a', fg='#22d3ee', font=('Consolas', 10))
        self.data_text.pack(fill='both', expand=True, padx=5, pady=5)

        frame_viz = tk.LabelFrame(workspace, text="Quantum Visualizer", bg='#1e293b', fg='#94a3b8', font=('Segoe UI', 11))
        workspace.add(frame_viz, width=600)

        self.viz_notebook = ttk.Notebook(frame_viz)
        self.viz_notebook.pack(fill='both', expand=True, padx=5, pady=5)

        self.canvas_landscape = tk.Canvas(self.viz_notebook, bg='#020617')
        self.viz_notebook.add(self.canvas_landscape, text="Energy Landscape (DOS)")

        self.canvas_pathway = tk.Canvas(self.viz_notebook, bg='#020617')
        self.viz_notebook.add(self.canvas_pathway, text="Reaction Pathway")

        frame_logs = tk.LabelFrame(workspace, text="Lab Notes & Protocol", bg='#1e293b', fg='#94a3b8', font=('Segoe UI', 11))
        workspace.add(frame_logs, width=500)

        self.log_text = scrolledtext.ScrolledText(frame_logs, bg='#0f172a', fg='#f8fafc', font=('Consolas', 10))
        self.log_text.pack(fill='both', expand=True, padx=5, pady=5)

        self.add_log(">> SYSTEM ONLINE - EXTENSIVE DATABASE LOADED.")

    def add_log(self, msg, color=None):
        self.log_text.insert('end', f"{msg}\n")
        self.log_text.see('end')
        self.root.update_idletasks()

    def on_system_select(self, event):
        self.add_log(f">> Selected: {self.atom_var.get()}")

    def generate_problem(self):
        try:
            selection = self.atom_var.get()
            if '---' in selection: return

            self.log_text.delete('1.0', 'end')
            self.data_text.delete('1.0', 'end')
            self.add_log(f">> GENERATING HAMILTONIAN FOR: {selection}")

            self.numbers = []
            self.number_labels = []

            # Handle pure atoms from dropdown (e.g. 'Gold (Au-197)')
            if selection in self.atomic_data:
                atom = self.atomic_data[selection]
                self.data_text.insert('end', f"Element: {selection}\n")
                self.data_text.insert('end', f"Protons (Z): {atom['Z']}\n")

                for shell_idx, shell_count in enumerate(atom['shells']):
                    base_energy = (atom['Z']**2) * (1.0 / ((shell_idx + 1)**2)) * 13.6 
                    base_energy = int(base_energy * 5)
                    shell_name = self.shell_names[shell_idx] if shell_idx < len(self.shell_names) else f"n={shell_idx+1}"
                    label = f"{atom['symbol']} {shell_name} orbital"
                    for _ in range(shell_count * 4):
                        val = max(5, int(base_energy + random.gauss(0, base_energy*0.1)))
                        self.numbers.append(val)
                        self.number_labels.append(label)

            # Handle molecules
            elif selection in self.molecular_data:
                mol = self.molecular_data[selection]
                self.data_text.insert('end', f"Formula: {mol['formula']}\n")

                for atom_name, count in mol['atoms']:
                    if atom_name in self.atomic_data:
                        atom = self.atomic_data[atom_name]
                        self.data_text.insert('end', f"  - {count}x {atom_name}\n")
                        for shell_idx, shell_count in enumerate(atom['shells']):
                            base_energy = (atom['Z']**2) * (1.0 / ((shell_idx + 1)**2)) * 13.6 
                            base_energy = int(base_energy * 5)
                            shell_name = self.shell_names[shell_idx] if shell_idx < len(self.shell_names) else f"n={shell_idx+1}"
                            label = f"{atom['symbol']} {shell_name} orbital"
                            for _ in range(count * shell_count * 2):
                                val = max(5, int(base_energy + random.gauss(0, base_energy*0.1)))
                                self.numbers.append(val)
                                self.number_labels.append(label)

                bond_count = len(mol['atoms']) * 3
                for _ in range(bond_count):
                    val = random.randint(50, 300)
                    self.numbers.append(val)
                    self.number_labels.append(f"Bonding Energy ({mol['formula']})")

            subset_size = min(len(self.numbers), 15)
            indices = random.sample(range(len(self.numbers)), subset_size)
            self.target = sum(self.numbers[i] for i in indices)

            self.data_text.insert('end', f"\nTotal Components: {len(self.numbers)}\n")
            self.data_text.insert('end', f"Target Eigenvalue: {self.target} keV\n")
            self.add_log(f">> System Ready. Target: {self.target} keV")
            self.add_log(">> Click 'Run Full Analysis' to solve.")

        except Exception as e:
            self.add_log(f"Error: {e}")

    def visualize_dos(self):
        self.canvas_landscape.delete('all')
        w = self.canvas_landscape.winfo_width()
        h = self.canvas_landscape.winfo_height()
        if not self.numbers: return

        bins = 50
        min_v, max_v = min(self.numbers), max(self.numbers)
        r = max_v - min_v if max_v > min_v else 1
        hist = [0] * bins
        for n in self.numbers:
            idx = int((n - min_v) / r * (bins-1))
            hist[idx] += 1
        max_h = max(hist) if max(hist) > 0 else 1
        bar_w = w / bins
        for i, count in enumerate(hist):
            x = i * bar_w
            y = h - (count / max_h) * (h - 20)
            self.canvas_landscape.create_rectangle(x, h, x+bar_w, y, fill='#3b82f6', outline='#1e293b')
        self.canvas_landscape.create_text(w/2, 20, text="Component Energy Distribution (DOS)", fill='white', font=('Segoe UI', 10))

    def visualize_pathway(self, sequence):
        self.canvas_pathway.delete('all')
        w = self.canvas_pathway.winfo_width()
        h = self.canvas_pathway.winfo_height()
        if not sequence: return

        self.canvas_pathway.create_line(40, h-40, w-20, h-40, fill='#94a3b8', width=2)
        self.canvas_pathway.create_line(40, h-40, 40, 20, fill='#94a3b8', width=2)

        step_w = (w - 80) / len(sequence)
        max_e = sum([x[0] for x in sequence]) * 1.3
        current_e = 0
        prev_x, prev_y = 40, h-40

        for i, (val, label) in enumerate(sequence):
            barrier = val * 0.3
            target_y = h - 40 - ((current_e + val) / max_e) * (h - 80)
            peak_y = h - 40 - ((current_e + val + barrier) / max_e) * (h - 80)
            next_x = 40 + (i+1) * step_w
            mid_x = (prev_x + next_x) / 2

            self.canvas_pathway.create_line(prev_x, prev_y, mid_x, peak_y, next_x, target_y, smooth=True, width=3, fill='#f43f5e')
            self.canvas_pathway.create_line(next_x-5, target_y, next_x+5, target_y, width=2, fill='#22d3ee')
            current_e += val
            prev_x, prev_y = next_x, target_y

        self.canvas_pathway.create_text(w/2, 20, text="Reaction Coordinate & Barriers", fill='white', font=('Segoe UI', 10))

    def solve_full_analysis(self):
        if not self.numbers: return
        self.add_log("\n>> INITIATING SOLVER PROTOCOL...")

        def run():
            items = list(zip(self.numbers, self.number_labels))
            items.sort(key=lambda x: x[0])
            dp = {0: True}
            parent = {0: None}

            for num, label in items:
                new_sums = {}
                for energy in dp:
                    if energy + num <= self.target and (energy + num) not in dp:
                        new_sums[energy+num] = True
                        parent[energy+num] = (energy, num, label)
                dp.update(new_sums)
                if self.target in dp: break

            if self.target in dp:
                path = []
                curr = self.target
                while curr != 0:
                    prev, n, l = parent[curr]
                    path.append((n, l))
                    curr = prev
                path.reverse()
                self.solution_path = path

                self.add_log("\n📦 INGREDIENTS IDENTIFIED:")
                counts = defaultdict(list)
                for n, l in path: counts[l].append(n)
                for label in sorted(counts.keys()):
                    vals = counts[label]
                    avg = sum(vals)/len(vals)
                    self.add_log(f"  • {len(vals)}x {label} (Avg: {avg:.1f} keV)")

                self.add_log("\n🔬 SMART LAB PROTOCOL:")
                # Heuristic Advice
                if any('Carbon' in l for n, l in path):
                    self.add_log("  > Synthesis Type: Organic Chemistry")
                    self.add_log("  > Precursor: Hydrocarbon feedstock.")
                elif any('Iron' in l or 'Copper' in l or 'Gold' in l for n, l in path):
                    self.add_log("  > Synthesis Type: Metallic/Alloy")
                    self.add_log("  > Precursor: Metal ore or salts.")
                else:
                    self.add_log("  > Synthesis Type: Inorganic Salt/Acid")

                self.visualize_dos()
                self.visualize_pathway(path)
            else:
                self.add_log(">> No exact solution found for this target.")

        threading.Thread(target=run, daemon=True).start()

    def reset(self):
        self.numbers = []
        self.log_text.delete('1.0', 'end')
        self.data_text.delete('1.0', 'end')
        self.canvas_landscape.delete('all')
        self.canvas_pathway.delete('all')
        self.add_log(">> System Reset.")

if __name__ == "__main__":
    root = tk.Tk()
    app = NuclearSSPSimulator(root)
    root.mainloop()
