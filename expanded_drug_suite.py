import tkinter as tk
from tkinter import ttk, scrolledtext
import random
import threading
import time
import math
from collections import defaultdict

class DrugDiscoverySimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("MedChem Studio - EXPANDED DRUG DATABASE")
        self.root.geometry("1700x1000")
        self.root.configure(bg='#0f172a')

        self.fragments = []
        self.fragment_labels = []
        self.target_affinity = 0
        self.solution_path = []

        # --- FRAGMENT LIBRARY ---
        self.fragment_db = {
            'Phenyl Ring (Ar)': {'base_e': 500, 'desc': 'Hydrophobic Core'},
            'Methyl Group (-CH3)': {'base_e': 50, 'desc': 'Lipophilic Spacer'},
            'Carboxyl (-COOH)': {'base_e': 180, 'desc': 'H-Bond Donor/Acceptor'},
            'Hydroxyl (-OH)': {'base_e': 120, 'desc': 'H-Bond Donor'},
            'Amine (-NH2)': {'base_e': 110, 'desc': 'Basic Center'},
            'Amide Link (-CONH-)': {'base_e': 250, 'desc': 'Peptide Bond Mimic'},
            'Ester Link (-COO-)': {'base_e': 220, 'desc': 'Metabolic Labile'},
            'Chlorine (-Cl)': {'base_e': 160, 'desc': 'Metabolic Blocker'},
            'Fluorine (-F)': {'base_e': 140, 'desc': 'Bio-isostere'},
            'Sulfonamide (-SO2NH2)': {'base_e': 350, 'desc': 'Polar Pharmacophore'},
            'Imidazole Ring': {'base_e': 450, 'desc': 'Heterocycle'},
            'Pyridine Ring': {'base_e': 460, 'desc': 'Heterocycle'},
            'Thiazole Ring': {'base_e': 470, 'desc': 'Sulfur Heterocycle'},
            'Beta-Lactam Ring': {'base_e': 600, 'desc': 'Antibiotic Warhead'},
            'Nitro Group (-NO2)': {'base_e': 200, 'desc': 'Electron Withdrawing'},
            'Ether Link (-O-)': {'base_e': 90, 'desc': 'H-Bond Acceptor'},
        }

        # --- EXPANDED DRUG DATABASE ---
        self.drug_db = {
            # --- PAIN & INFLAMMATION ---
            'Aspirin (Analgesic)': {'class': 'NSAID', 'structure': [('Phenyl Ring (Ar)', 1), ('Carboxyl (-COOH)', 1), ('Ester Link (-COO-)', 1), ('Methyl Group (-CH3)', 1)]},
            'Tylenol (Acetaminophen)': {'class': 'Analgesic', 'structure': [('Phenyl Ring (Ar)', 1), ('Hydroxyl (-OH)', 1), ('Amide Link (-CONH-)', 1), ('Methyl Group (-CH3)', 1)]},
            'Advil (Ibuprofen)': {'class': 'NSAID', 'structure': [('Phenyl Ring (Ar)', 1), ('Carboxyl (-COOH)', 1), ('Methyl Group (-CH3)', 4)]},
            'Morphine (Opioid)': {'class': 'Opioid Analgesic', 'structure': [('Phenyl Ring (Ar)', 1), ('Hydroxyl (-OH)', 2), ('Amine (-NH2)', 1), ('Ether Link (-O-)', 1), ('Methyl Group (-CH3)', 1)]},

            # --- MENTAL HEALTH ---
            'Prozac (Fluoxetine)': {'class': 'SSRI', 'structure': [('Phenyl Ring (Ar)', 2), ('Amine (-NH2)', 1), ('Fluorine (-F)', 3), ('Ether Link (-O-)', 1), ('Methyl Group (-CH3)', 1)]},
            'Valium (Diazepam)': {'class': 'Benzodiazepine', 'structure': [('Phenyl Ring (Ar)', 2), ('Chlorine (-Cl)', 1), ('Amide Link (-CONH-)', 1), ('Methyl Group (-CH3)', 1)]},
            'Xanax (Alprazolam)': {'class': 'Benzodiazepine', 'structure': [('Phenyl Ring (Ar)', 2), ('Chlorine (-Cl)', 1), ('Methyl Group (-CH3)', 1), ('Amide Link (-CONH-)', 1)]},
            'Adderall (Amphetamine)': {'class': 'Stimulant', 'structure': [('Phenyl Ring (Ar)', 1), ('Amine (-NH2)', 1), ('Methyl Group (-CH3)', 1)]},

            # --- ANTIBIOTICS ---
            'Penicillin G': {'class': 'Beta-Lactam', 'structure': [('Beta-Lactam Ring', 1), ('Phenyl Ring (Ar)', 1), ('Carboxyl (-COOH)', 1), ('Amide Link (-CONH-)', 1), ('Sulfur Heterocycle', 1)]},
            'Amoxicillin': {'class': 'Beta-Lactam', 'structure': [('Beta-Lactam Ring', 1), ('Phenyl Ring (Ar)', 1), ('Hydroxyl (-OH)', 1), ('Amine (-NH2)', 1), ('Carboxyl (-COOH)', 1)]},
            'Cipro (Ciprofloxacin)': {'class': 'Fluoroquinolone', 'structure': [('Phenyl Ring (Ar)', 2), ('Fluorine (-F)', 1), ('Carboxyl (-COOH)', 1), ('Amine (-NH2)', 1)]},

            # --- STOMACH & ALLERGY ---
            'Zantac (Ranitidine)': {'class': 'H2 Blocker', 'structure': [('Amine (-NH2)', 2), ('Nitro Group (-NO2)', 1), ('Sulfur Heterocycle', 1), ('Methyl Group (-CH3)', 3)]},
            'Benadryl (Diphenhydramine)': {'class': 'Antihistamine', 'structure': [('Phenyl Ring (Ar)', 2), ('Ether Link (-O-)', 1), ('Amine (-NH2)', 1), ('Methyl Group (-CH3)', 2)]},
            'Claritin (Loratadine)': {'class': 'Antihistamine', 'structure': [('Phenyl Ring (Ar)', 3), ('Chlorine (-Cl)', 1), ('Ester Link (-COO-)', 1), ('Amine (-NH2)', 1)]},

            # --- HEART & BLOOD ---
            'Lipitor (Atorvastatin)': {'class': 'Statin', 'structure': [('Phenyl Ring (Ar)', 3), ('Amide Link (-CONH-)', 1), ('Carboxyl (-COOH)', 1), ('Hydroxyl (-OH)', 2), ('Fluorine (-F)', 1)]},
            'Plavix (Clopidogrel)': {'class': 'Antiplatelet', 'structure': [('Phenyl Ring (Ar)', 1), ('Thiazole Ring', 1), ('Chlorine (-Cl)', 1), ('Ester Link (-COO-)', 1), ('Methyl Group (-CH3)', 1)]},

            # --- MISC ---
            'Caffeine': {'class': 'Stimulant', 'structure': [('Imidazole Ring', 1), ('Amide Link (-CONH-)', 2), ('Methyl Group (-CH3)', 3)]},
            'Viagra (Sildenafil)': {'class': 'PDE5 Inhibitor', 'structure': [('Phenyl Ring (Ar)', 2), ('Sulfonamide (-SO2NH2)', 1), ('Pyridine Ring', 1), ('Methyl Group (-CH3)', 2), ('Ether Link (-O-)', 1)]},
        }

        # Mapping friendly names for missing complex heterocycles
        # If a drug needs a ring not in DB, map to closest proxy
        self.fragment_db['Sulfur Heterocycle'] = {'base_e': 480, 'desc': 'Thiophene-like'}

        self.setup_ui()

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use('clam')

        header = tk.Frame(self.root, bg='#1e293b', height=70)
        header.pack(fill='x')
        tk.Label(header, text="💊 MedChem Studio - EXPANDED DB", 
                font=('Segoe UI', 22, 'bold'), bg='#1e293b', fg='#22d3ee').pack(pady=15)

        controls = tk.Frame(self.root, bg='#334155', padx=15, pady=15)
        controls.pack(fill='x', padx=15, pady=10)

        tk.Label(controls, text="Target Drug Profile:", bg='#334155', fg='white', font=('Arial', 11)).pack(side='left', padx=5)

        self.drug_var = tk.StringVar(value="Penicillin G")
        self.drug_dropdown = ttk.Combobox(controls, textvariable=self.drug_var, width=45, state='readonly', font=('Arial', 11))

        # Sort keys for dropdown
        self.drug_dropdown['values'] = sorted(list(self.drug_db.keys()))
        self.drug_dropdown.pack(side='left', padx=10)

        tk.Button(controls, text="1. Load Fragment Library", command=self.generate_fragments,
                 bg='#10b981', fg='white', font=('Segoe UI', 10, 'bold')).pack(side='left', padx=10)

        tk.Button(controls, text="2. Run Docking Simulation", command=self.run_docking,
                 bg='#8b5cf6', fg='white', font=('Segoe UI', 10, 'bold')).pack(side='left', padx=5)

        tk.Button(controls, text="Reset", command=self.reset,
                 bg='#64748b', fg='white').pack(side='right', padx=10)

        workspace = tk.PanedWindow(self.root, orient='horizontal', bg='#0f172a')
        workspace.pack(fill='both', expand=True, padx=15, pady=5)

        frame_specs = tk.LabelFrame(workspace, text="Compound Specifications", bg='#1e293b', fg='#94a3b8', font=('Segoe UI', 11, 'bold'))
        workspace.add(frame_specs, width=400)
        self.spec_text = scrolledtext.ScrolledText(frame_specs, bg='#0f172a', fg='#22d3ee', font=('Consolas', 10))
        self.spec_text.pack(fill='both', expand=True, padx=5, pady=5)

        frame_viz = tk.LabelFrame(workspace, text="Receptor Binding Site", bg='#1e293b', fg='#94a3b8', font=('Segoe UI', 11, 'bold'))
        workspace.add(frame_viz, width=700)
        self.canvas = tk.Canvas(frame_viz, bg='#020617')
        self.canvas.pack(fill='both', expand=True, padx=5, pady=5)

        frame_log = tk.LabelFrame(workspace, text="Retro-Synthesis Log", bg='#1e293b', fg='#94a3b8', font=('Segoe UI', 11, 'bold'))
        workspace.add(frame_log, width=500)
        self.log_text = scrolledtext.ScrolledText(frame_log, bg='#0f172a', fg='#f8fafc', font=('Consolas', 10))
        self.log_text.pack(fill='both', expand=True, padx=5, pady=5)

        self.add_log(">> DATABASE EXPANDED.")
        self.add_log(">> Added Antibiotics, Antihistamines, Opioids, and more.")

    def add_log(self, msg):
        self.log_text.insert('end', f"{msg}\n")
        self.log_text.see('end')
        self.root.update_idletasks()

    def generate_fragments(self):
        selection = self.drug_var.get()
        self.log_text.delete('1.0', 'end')
        self.spec_text.delete('1.0', 'end')

        if selection not in self.drug_db: return

        drug_info = self.drug_db[selection]
        self.spec_text.insert('end', f"Compound: {selection}\n")
        self.spec_text.insert('end', f"Class: {drug_info['class']}\n")
        self.spec_text.insert('end', "-"*30 + "\n")
        self.spec_text.insert('end', "PHARMACOPHORES:\n")

        self.fragments = []
        self.fragment_labels = []

        for frag_name, count in drug_info['structure']:
            if frag_name in self.fragment_db:
                data = self.fragment_db[frag_name]
                self.spec_text.insert('end', f"  - {count}x {frag_name}\n")
                self.spec_text.insert('end', f"    ({data['desc']})\n")

                for _ in range(count):
                    val = int(data['base_e'] + random.randint(-5, 5))
                    self.fragments.append(val)
                    self.fragment_labels.append(frag_name)
            else:
                self.spec_text.insert('end', f"  - {count}x {frag_name} (Unknown)\n")

        for _ in range(15):
            decoy_name = random.choice(list(self.fragment_db.keys()))
            val = int(self.fragment_db[decoy_name]['base_e'] + random.randint(-20, 20))
            self.fragments.append(val)
            self.fragment_labels.append(f"Decoy: {decoy_name}")

        self.target_affinity = sum([f for i, f in enumerate(self.fragments) if "Decoy" not in self.fragment_labels[i]])

        self.spec_text.insert('end', "\nTotal Binding Affinity Target:\n")
        self.spec_text.insert('end', f"{self.target_affinity} kcal/mol (simulated)")
        self.add_log(f">> Fragments Generated: {len(self.fragments)}")
        self.visualize_site_empty()

    def visualize_site_empty(self):
        self.canvas.delete('all')
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        self.canvas.create_oval(w/2-100, h/2-100, w/2+100, h/2+100, outline='#334155', width=3, dash=(5,5))
        self.canvas.create_text(w/2, h/2, text="Receptor Pocket\n(Unoccupied)", fill='#64748b', font=('Arial', 14))

    def visualize_docking(self, path):
        self.canvas.delete('all')
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w < 100: w=700
        if h < 100: h=500

        # Protein Surface
        self.canvas.create_arc(50, 50, w-50, h-50, start=0, extent=180, style='arc', outline='#94a3b8', width=4)
        self.canvas.create_text(w/2, 30, text="Biological Target (Protein)", fill='#94a3b8')

        cx, cy = w/2, h/2 + 50
        total_steps = len(path)

        for i, (energy, label) in enumerate(path):
            angle = i * (360 / total_steps)
            rad = 60 + (i * 12)
            x = cx + math.cos(math.radians(angle)) * rad
            y = cy + math.sin(math.radians(angle)) * rad

            color = '#10b981' 
            if 'Fluorine' in label or 'Chlorine' in label: color = '#ef4444'
            if 'Ring' in label: color = '#3b82f6'
            if 'Lactam' in label: color = '#f59e0b' # Special color for antibiotics

            if i > 0:
                prev_angle = (i-1) * (360 / total_steps)
                prev_rad = 60 + ((i-1) * 12)
                px = cx + math.cos(math.radians(prev_angle)) * prev_rad
                py = cy + math.sin(math.radians(prev_angle)) * prev_rad
                self.canvas.create_line(px, py, x, y, fill='white', width=2)

            self.canvas.create_oval(x-18, y-18, x+18, y+18, fill=color, outline='white')
            self.canvas.create_text(x, y, text=str(i+1), fill='white', font=('Arial', 9, 'bold'))
            self.canvas.create_text(x+25, y, text=label.split('(')[0], fill='#cbd5e1', font=('Arial', 8), anchor='w')

    def run_docking(self):
        if not self.fragments: return
        self.add_log("\n>> RUNNING DOCKING ALGORITHM...")

        def run():
            items = list(zip(self.fragments, self.fragment_labels))
            items.sort(key=lambda x: x[0], reverse=True)

            dp = {0: True}
            parent = {0: None}

            for num, label in items:
                new_sums = {}
                for energy in dp:
                    if energy + num <= self.target_affinity and (energy + num) not in dp:
                        new_sums[energy+num] = True
                        parent[energy+num] = (energy, num, label)
                dp.update(new_sums)
                if self.target_affinity in dp: break

            if self.target_affinity in dp:
                path = []
                curr = self.target_affinity
                while curr != 0:
                    prev, n, l = parent[curr]
                    path.append((n, l))
                    curr = prev
                self.solution_path = path 

                self.add_log("\n✅ CONFORMATION LOCKED")
                self.add_log(f"   Match Score: {self.target_affinity}")
                self.add_log("\n🧩 ASSEMBLY SEQUENCE:")
                for i, (energy, label) in enumerate(path, 1):
                    self.add_log(f"   {i}. {label}")

                # Advanced ADMET
                self.add_log("\n⚠️ ADMET ANALYSIS:")
                rings = sum(1 for _, l in path if 'Ring' in l)
                polars = sum(1 for _, l in path if 'Hydroxyl' in l or 'Amine' in l or 'Carboxyl' in l)
                halogen = sum(1 for _, l in path if '-F' in l or '-Cl' in l)

                if rings >= 3 and polars < 2:
                    self.add_log("   • Absorption: Poor (Too Lipophilic)")
                elif polars >= 3:
                    self.add_log("   • Absorption: Good (Water Soluble)")
                else:
                    self.add_log("   • Absorption: Moderate")

                if halogen > 0:
                    self.add_log("   • Metabolic Stability: Enhanced")

                if any('Lactam' in l for _, l in path):
                    self.add_log("   • Mechanism: Cell Wall Synthesis Inhibitor")

                self.visualize_docking(path)
            else:
                self.add_log("❌ DOCKING FAILED.")

        threading.Thread(target=run, daemon=True).start()

    def reset(self):
        self.fragments = []
        self.log_text.delete('1.0', 'end')
        self.spec_text.delete('1.0', 'end')
        self.canvas.delete('all')
        self.add_log(">> Reset Complete.")

if __name__ == "__main__":
    root = tk.Tk()
    app = DrugDiscoverySimulator(root)
    root.mainloop()
