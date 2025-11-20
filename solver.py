import numpy as np
import math
import warnings
import sys

sys.setrecursionlimit(2000)
warnings.filterwarnings("ignore")

# ==========================================
# 1. ASTRONOMICAL PHYSICS KERNEL
# ==========================================

class AstroDomain:
    def __init__(self, name, initial_scale=10.0):
        self.name = name
        # Initialize safely
        self.val = np.random.uniform(initial_scale / 10, initial_scale * 10) 
        self.velocity = 0.0
        
    def update_multiplicative(self, factor, dt):
        """
        Updates value by a multiplicative factor (safe for huge numbers).
        val_new = val_old * (1 + speed * dt)
        """
        # Damping on the factor itself to prevent oscillation
        # We treat 'velocity' here as 'rate of exponential growth'
        target_velocity = factor
        self.velocity = (self.velocity * 0.8) + (target_velocity * 0.2)
        
        # Cap the step size to 10% growth per tick to ensure stability
        step_change = np.clip(self.velocity * dt, -0.1, 0.1)
        
        # Apply update: val = val * (1 + change)
        try:
            self.val *= (1.0 + step_change)
        except OverflowError:
            self.val = float('inf')

        # Safety floor
        if self.val < 1e-100: self.val = 1e-100

# ==========================================
# 2. LOG-SCALE MATH ENGINE
# ==========================================

class AstroPhysicsSolver:
    def __init__(self):
        self.variables = {}
        
    def create_var(self, name, rough_magnitude):
        self.variables[name] = AstroDomain(name, initial_scale=rough_magnitude)
        
    def solve(self, equation, steps=100000):
        print(f"\n[Physics Engine] Target Equation: {equation}")
        
        lhs_str, rhs_str = equation.split('=')
        
        # 1. Parse Target Safely
        try:
            # Use string replacement for scientific notation "1e300"
            target_val = float(eval(rhs_str))
        except OverflowError:
            target_val = float('inf')
            print("Warning: Target is infinite.")
        
        if target_val == float('inf'):
            print("[System] Target too large for 64-bit float. Stopping.")
            return {}

        # Work in Log10 Space
        if target_val > 0:
            log_target = math.log10(target_val)
        else:
            log_target = -100
            
        print(f"[System] Target Magnitude: 10^{log_target:.2f}")
            
        # 2. Initialize Variables
        import re
        tokens = set(re.findall(r'[a-zA-Z_]+', lhs_str))
        num_vars = len(tokens) if len(tokens) > 0 else 1
        
        # Guess start magnitude (e.g. target 10^300, vars should be 10^100)
        estimated_scale = 10 ** (log_target / num_vars)
        
        for t in tokens: 
            if t not in self.variables: 
                self.create_var(t, rough_magnitude=estimated_scale)
            
        # 3. Annealing Loop
        for t in range(steps):
            vals = {n: d.val for n, d in self.variables.items()}
            
            # Evaluate LHS
            try:
                current_lhs = eval(lhs_str, {}, vals)
            except OverflowError:
                current_lhs = float('inf')
            
            # Current Log Magnitude
            if current_lhs <= 0: current_lhs = 1e-100
            try:
                log_current = math.log10(current_lhs)
            except ValueError:
                log_current = -100
                
            # ERROR: Difference in Orders of Magnitude
            error = log_current - log_target
            
            # Exit condition (Precision to 8 decimal places of exponent)
            if abs(error) < 1e-8:
                break
                
            # 4. Sensitivity Analysis (Gradient Free)
            # We determine power law relationship without exploding math.
            # How much does LHS change if input changes by 0.1%?
            perturbation = 1.001 # 0.1% change
            log_perturb_delta = math.log10(perturbation) # Constant small number
            
            for name in tokens:
                domain = self.variables[name]
                orig = domain.val
                
                # Test perturbation
                domain.val = orig * perturbation
                
                vals_new = {n: v.val for n, v in self.variables.items()}
                try:
                    lhs_new = eval(lhs_str, {}, vals_new)
                    if lhs_new <= 0: lhs_new = 1e-100
                    log_new = math.log10(lhs_new)
                except:
                    log_new = log_current # No change detected
                
                # Calculate Power Sensitivity (Slope in Log-Log space)
                # E.g., for x^2, sensitivity is 2. For x^3, it is 3.
                sensitivity = (log_new - log_current) / log_perturb_delta
                
                # Restore Value
                domain.val = orig
                
                # 5. Apply Force (Multiplicative)
                # If error is + (too high), we shrink. If - (too low), we grow.
                # We divide by sensitivity: x^3 needs smaller adjustments than x^1.
                if abs(sensitivity) < 0.001: sensitivity = 1.0 # Avoid div by zero
                
                force = -error / sensitivity 
                
                # Scale force for simulation stability
                force *= 10.0 
                
                domain.update_multiplicative(force, dt=0.01)
        
        return {n: d.val for n, d in self.variables.items()}

# ==========================================
# 3. ASTRONOMICAL DEMONSTRATION
# ==========================================

if __name__ == "__main__":
    solver = AstroPhysicsSolver()

    # TEST 2: Multi-variable factorization of huge number
    # x * y = 1e200
    solver = AstroPhysicsSolver()
    res2 = solver.solve("x * y = 1e200")
    if 'x' in res2:
        print(f"\nResult x: {res2['x']:.4e}")
        print(f"Result y: {res2['y']:.4e}")
        print(f"Product:  {res2['x'] * res2['y']:.4e}")
