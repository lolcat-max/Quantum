import tkinter as tk
from tkinter import ttk, scrolledtext
import math
import random
import threading
import time
from collections import defaultdict

class MaterialDesignEngine:
    def __init__(self, root):
        self.root = root
        self.root.title("Material Design Engine - EXACT DP ALLOY SOLVER")
        self.root.geometry("1750x1000")
        self.root.configure(bg='#111')

        self.target_prop = 0
        self.solution_mix = []
        self.rotation_y = 0
        self.running_viz = False

        # --- ELEMENTAL DATABASE ---
        # Properties normalized for the "Game/Sim":
        # Density (g/cm3), Modulus (GPa), Melting Pt (K), Radius (pm), Color
        self.elements = {
            'Titanium (Ti)': {'d': 4.5, 'E': 116, 'mp': 1941, 'r': 140, 'c': '#a1a1a1'},
            'Aluminum (Al)': {'d': 2.7, 'E': 69, 'mp': 933, 'r': 125, 'c': '#e6e6e6'},
            'Vanadium (V)':  {'d': 6.1, 'E': 128, 'mp': 2183, 'r': 135, 'c': '#a6a6a6'},
            'Chromium (Cr)': {'d': 7.19, 'E': 279, 'mp': 2180, 'r': 140, 'c': '#8a99c7'},
            'Iron (Fe)':     {'d': 7.87, 'E': 211, 'mp': 1811, 'r': 140, 'c': '#e06666'},
            'Nickel (Ni)':   {'d': 8.90, 'E': 200, 'mp': 1728, 'r': 135, 'c': '#ffd966'},
            'Copper (Cu)':   {'d': 8.96, 'E': 130, 'mp': 1357, 'r': 135, 'c': '#d98850'},
            'Tungsten (W)':  {'d': 19.25, 'E': 411, 'mp': 3695, 'r': 135, 'c': '#444444'},
            'Carbon (C)':    {'d': 2.26, 'E': 300, 'mp': 3800, 'r': 70, 'c': '#111111'}, # Interstitial
            'Silicon (Si)':  {'d': 2.33, 'E': 150, 'mp': 1687, 'r': 110, 'c': '#5e6e7e'},
        }

        self.setup_ui()

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use('clam')

        header = tk.Frame(self.root, bg='#222', height=80)
        header.pack(fill='x')
        tk.Label(header, text="💎 MATERIAL DESIGN ENGINE - EXACT DP", 
                font=('Impact', 24), bg='#222', fg='#00ff99').pack(pady=20)

        controls = tk.Frame(self.root, bg='#333', padx=20, pady=20)
        controls.pack(fill='x', padx=20, pady=10)

        tk.Label(controls, text="Target Property:", bg='#333', fg='white').pack(side='left')
        self.prop_var = tk.StringVar(value="Elastic Modulus (GPa)")
        ttk.Combobox(controls, textvariable=self.prop_var, values=['Density (g/cm3)', 'Elastic Modulus (GPa)', 'Melting Pt (K)'], state='readonly').pack(side='left', padx=10)

        tk.Label(controls, text="Target Value:", bg='#333', fg='white').pack(side='left')
        self.val_var = tk.StringVar(value="150")
        tk.Entry(controls, textvariable=self.val_var, width=10).pack(side='left', padx=5)

        tk.Button(controls, text="1. SOLVE ALLOY MIX (DP)", command=self.run_dp_design,
                 bg='#00bfff', fg='black', font=('Arial', 10, 'bold')).pack(side='left', padx=20)

        tk.Button(controls, text="2. GENERATE 3D LATTICE", command=self.run_viz,
                 bg='#ff00ff', fg='black', font=('Arial', 10, 'bold')).pack(side='left', padx=5)

        workspace = tk.PanedWindow(self.root, orient='horizontal', bg='#000')
        workspace.pack(fill='both', expand=True, padx=20, pady=10)

        # Left: 3D Viz
        frame_viz = tk.LabelFrame(workspace, text="Crystal Lattice Visualization", bg='#111', fg='#00ff99')
        workspace.add(frame_viz, width=1100)
        self.canvas = tk.Canvas(frame_viz, bg='black')
        self.canvas.pack(fill='both', expand=True)

        # Right: Data
        frame_data = tk.LabelFrame(workspace, text="Material Properties Log", bg='#111', fg='#00ff99')
        workspace.add(frame_data, width=500)
        self.log_text = scrolledtext.ScrolledText(frame_data, bg='#0a0a0a', fg='#00ff99', font=('Consolas', 11))
        self.log_text.pack(fill='both', expand=True, padx=5, pady=5)

    def log(self, msg):
        self.log_text.insert('end', f"{msg}\n")
        self.log_text.see('end')
        self.root.update_idletasks()

    def run_dp_design(self):
        try:
            target = float(self.val_var.get())
        except: return

        mode = self.prop_var.get()
        key_map = {'Density (g/cm3)': 'd', 'Elastic Modulus (GPa)': 'E', 'Melting Pt (K)': 'mp'}
        key = key_map[mode]

        self.log_text.delete('1.0', 'end')
        self.log(f"Designing Alloy for {mode} = {target}...")

        # DP PROBLEM:
        # We want a unit cell (e.g., 8 atoms) where average property matches target.
        # Or simpler: Find a combination of atoms whose sum = target * count.
        # Let's assume a standard BCC/FCC unit cell of 10 atoms for simulation precision.

        cell_size = 10
        target_sum = target * cell_size

        # Prepare items (Weight = Property Value, Value = Name)
        # We use integers for DP (multiply by 100)
        pool = []
        for name, props in self.elements.items():
            val = props[key]
            # Allow multiple of each element (up to cell size)
            for _ in range(cell_size):
                pool.append((int(val * 10), name)) # Scale by 10 for int math

        scaled_target = int(target_sum * 10)

        # DP Solver (Exact Subset Sum with specific count constraint is hard, 
        # but we can use standard subset sum and check count later or use a simplified greedy/random search if DP is too slow for this specific constraint).
        # For "Exact DP", let's use a recursive memoized solver for exact N items.

        self.log(f">> Solving for sum {scaled_target} with {cell_size} atoms...")

        memo = {}
        pool.sort(key=lambda x: x[0], reverse=True) # Optimization

        def solve(idx, count, current_sum):
            state = (idx, count, current_sum)
            if state in memo: return memo[state]

            if count == 0:
                return [] if current_sum == 0 else None

            if current_sum < 0 or idx >= len(pool):
                return None

            # Option 1: Include current atom
            val, name = pool[idx]
            res = solve(idx + 1, count - 1, current_sum - val)
            if res is not None:
                res.append(name)
                memo[state] = res
                return res

            # Option 2: Skip
            res = solve(idx + 1, count, current_sum)
            if res is not None:
                memo[state] = res
                return res

            memo[state] = None
            return None

        # To make it faster for demo, we use a simplified search or allow variance
        # Solving exact subset sum for N items is O(N*S).
        # Let's try a randomized hill climber which is often used in material design ("Genetic Algorithm"),
        # but since user asked for DP, we'll try a small DP depth or fallback.

        # ACTUALLY, simpler approach for DP Exact: 
        # dp[k][w] = boolean (can we make weight w with k items?)

        # Limit range to keep it fast
        # Scale target down? No, let's use the recursion with a timeout wrapper.

        solution = None

        # Try simplified DP: Unbounded Knapsack style (can repeat items)
        # dp[w] = min_items needed. We want exactly cell_size.

        # Let's go with the Recursive Search above but strictly limited
        start_t = time.time()
        solution = solve(0, cell_size, scaled_target)

        if not solution:
            # Try finding closest match
            self.log("Exact match not found. Optimizing...")
            best_diff = float('inf')
            best_mix = []

            for _ in range(5000): # Monte Carlo fallback
                mix = random.choices(list(self.elements.keys()), k=cell_size)
                s = sum(self.elements[m][key] for m in mix)
                diff = abs(s - target_sum)
                if diff < best_diff:
                    best_diff = diff
                    best_mix = mix
                    if diff < 0.1: break
            solution = best_mix

        self.solution_mix = solution

        # Analysis
        self.log(f"\n✅ ALLOY COMPOSITION DESIGNED:")
        counts = defaultdict(int)
        for el in solution: counts[el] += 1

        total_d = 0
        total_E = 0
        for el in solution:
            total_d += self.elements[el]['d']
            total_E += self.elements[el]['E']

        avg_d = total_d / cell_size
        avg_E = total_E / cell_size

        for el, c in counts.items():
            pct = (c/cell_size)*100
            self.log(f"  • {el}: {pct:.0f}%")

        self.log(f"\nPredicted Properties:")
        self.log(f"  Density: {avg_d:.2f} g/cm3")
        self.log(f"  Modulus: {avg_E:.2f} GPa")

    def run_viz(self):
        if not self.solution_mix: return

        self.running_viz = True
        self.canvas.delete('all')

        # Generate 3D lattice positions (BCC Structure 3x3x3)
        lattice_points = []
        mix = self.solution_mix.copy()

        # Fill a 3x3x3 grid (27 atoms), repeating the mix pattern
        count = 0
        for x in range(-1, 2):
            for y in range(-1, 2):
                for z in range(-1, 2):
                    el = mix[count % len(mix)]
                    count += 1
                    color = self.elements[el]['c']
                    radius = self.elements[el]['r'] / 10 # Scale

                    lattice_points.append({
                        'x': x * 60, 'y': y * 60, 'z': z * 60,
                        'c': color, 'r': radius
                    })

        def render_loop():
            while self.running_viz:
                self.rotation_y += 0.02
                self.render_3d(lattice_points)
                time.sleep(0.03)

        threading.Thread(target=render_loop, daemon=True).start()

    def render_3d(self, points):
        try:
            self.canvas.delete('all')
            w = self.canvas.winfo_width()
            h = self.canvas.winfo_height()
            cx, cy = w/2, h/2

            projected = []
            cos_y = math.cos(self.rotation_y)
            sin_y = math.sin(self.rotation_y)

            for p in points:
                # Rotate Y
                x = p['x'] * cos_y - p['z'] * sin_y
                z = p['z'] * cos_y + p['x'] * sin_y
                y = p['y']

                # Project
                scale = 400 / (400 + z + 200) # Perspective
                sx = cx + x * scale
                sy = cy + y * scale
                sr = p['r'] * scale

                projected.append((z, sx, sy, sr, p['c']))

            # Sort Painter's Algo
            projected.sort(key=lambda x: x[0], reverse=True)

            # Draw connections (Lattice bonds)
            # Simplified: just draw atoms

            for z, sx, sy, sr, c in projected:
                self.canvas.create_oval(sx-sr, sy-sr, sx+sr, sy+sr, fill=c, outline='black')
                # Shine
                self.canvas.create_oval(sx-sr*0.4, sy-sr*0.4, sx, sy, fill='white', outline='')

        except: pass

if __name__ == "__main__":
    root = tk.Tk()
    app = MaterialDesignEngine(root)
    root.mainloop()