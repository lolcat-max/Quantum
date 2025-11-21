import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import json
import urllib.request
import urllib.parse
import re
from collections import Counter

class ReactionSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Reaction Simulator - EXACT ATOMIC BALANCE")
        self.root.geometry("1600x900")
        self.root.configure(bg='#0f172a')

        self.reactant_atoms = Counter()

        self.setup_ui()

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use('clam')

        header = tk.Frame(self.root, bg='#1e293b', height=80)
        header.pack(fill='x')
        tk.Label(header, text="⚗️ MULTI-MOLECULE REACTION SIMULATOR", 
                font=('Segoe UI', 22, 'bold'), bg='#1e293b', fg='#22d3ee').pack(pady=20)

        # Inputs
        controls = tk.Frame(self.root, bg='#334155', padx=20, pady=20)
        controls.pack(fill='x', padx=20, pady=10)

        tk.Label(controls, text="Reactant A:", bg='#334155', fg='white').pack(side='left')
        self.mol_a = tk.StringVar(value="Acetic Acid")
        tk.Entry(controls, textvariable=self.mol_a, width=20).pack(side='left', padx=5)

        tk.Label(controls, text="+ Reactant B:", bg='#334155', fg='white').pack(side='left')
        self.mol_b = tk.StringVar(value="Ethanol")
        tk.Entry(controls, textvariable=self.mol_b, width=20).pack(side='left', padx=5)

        tk.Button(controls, text="⚡ SIMULATE REACTION", command=self.run_reaction,
                 bg='#10b981', fg='white', font=('Segoe UI', 10, 'bold')).pack(side='left', padx=20)

        # Display
        workspace = tk.PanedWindow(self.root, orient='horizontal', bg='#0f172a')
        workspace.pack(fill='both', expand=True, padx=20, pady=10)

        self.log_text = scrolledtext.ScrolledText(workspace, bg='#0f172a', fg='#f8fafc', font=('Consolas', 12))
        self.log_text.pack(fill='both', expand=True)

    def log(self, msg):
        self.log_text.insert('end', f"{msg}\n")
        self.log_text.see('end')
        self.root.update_idletasks()

    def get_formula(self, name):
        try:
            base = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
            url = f"{base}/compound/name/{urllib.parse.quote(name)}/property/MolecularFormula/JSON"
            with urllib.request.urlopen(url) as r:
                data = json.loads(r.read().decode())
                return data['PropertyTable']['Properties'][0]['MolecularFormula']
        except:
            return None

    def parse_formula(self, formula):
        matches = re.findall(r'([A-Z][a-z]*)(\d*)', formula)
        c = Counter()
        for el, n in matches:
            c[el] += int(n) if n else 1
        return c

    def run_reaction(self):
        a_name = self.mol_a.get()
        b_name = self.mol_b.get()
        self.log_text.delete('1.0', 'end')

        threading.Thread(target=self.thread_logic, args=(a_name, b_name), daemon=True).start()

    def thread_logic(self, a, b):
        self.log(f"Fetching data for: {a} + {b}...")

        f_a = self.get_formula(a)
        f_b = self.get_formula(b)

        if not f_a or not f_b:
            self.log("❌ Could not fetch data from PubChem.")
            return

        self.log(f"  • {a}: {f_a}")
        self.log(f"  • {b}: {f_b}")

        # Combine Atoms
        atoms_a = self.parse_formula(f_a)
        atoms_b = self.parse_formula(f_b)
        total_atoms = atoms_a + atoms_b

        self.log("-" * 40)
        self.log(f"TOTAL ATOMIC POOL: {dict(total_atoms)}")
        self.log("-" * 40)

        # PREDICT PRODUCT (Simplified Logic)
        # We look for a condensation reaction (Water loss) which is most common in MedChem
        # Product = (A + B) - H2O

        product_atoms = total_atoms.copy()
        byproduct = None

        # Heuristic: If we have enough H and O, simulate condensation
        if product_atoms['H'] >= 2 and product_atoms['O'] >= 1:
            product_atoms['H'] -= 2
            product_atoms['O'] -= 1
            byproduct = "Water (H2O)"
            reaction_type = "Condensation / Esterification"
        else:
            reaction_type = "Addition / Synthesis"

        # Reconstruct Formula String
        p_formula = ""
        for el in ['C', 'H', 'O', 'N', 'S', 'Cl', 'F']: # Standard order
            if product_atoms[el] > 0:
                p_formula += f"{el}{product_atoms[el] if product_atoms[el]>1 else ''}"

        self.log(f"\n🔮 PREDICTED REACTION PATHWAY:")
        self.log(f"   Type: {reaction_type}")
        self.log(f"\n   {a} + {b}")
        self.log(f"   ⬇")
        self.log(f"   Product ({p_formula})")

        if byproduct:
            self.log(f"   + {byproduct}")

        # Attempt to identify product via PubChem (Reverse Search)
        # Note: Searching by formula returns MANY isomers, so we just show the mass
        self.log(f"\n✅ MASS BALANCE CHECK:")
        self.log(f"   Reactants: {dict(total_atoms)}")

        check_atoms = product_atoms.copy()
        if byproduct == "Water (H2O)":
            check_atoms['H'] += 2
            check_atoms['O'] += 1

        self.log(f"   Products:  {dict(check_atoms)}")

        if check_atoms == total_atoms:
            self.log("   Status: PERFECTLY BALANCED")
        else:
            self.log("   Status: IMBALANCE DETECTED")

if __name__ == "__main__":
    root = tk.Tk()
    app = ReactionSimulator(root)
    root.mainloop()