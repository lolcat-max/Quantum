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
        # Initialize to scale for better convergence on balanced factors
        self.val = initial_scale
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
    
    def _find_integer_factors(self, target_int, approx_x, approx_y, search_radius=20):
        """
        For integer targets and simple x * y = N equations, find exact integer factors
        close to the approximate floating-point solutions, prioritizing balance.
        Assumes two variables x and y, with x <= y.
        """
        if target_int <= 0:
            return None
        
        # Ensure approx_x <= approx_y for consistency
        if approx_x > approx_y:
            approx_x, approx_y = approx_y, approx_x
        
        best_pair = None
        min_diff = float('inf')
        
        # Local search near approximations for balanced factors
        start = max(1, int(approx_x) - search_radius)
        end = min(int(approx_x) + search_radius, int(math.sqrt(target_int)) + 1)
        
        for cand_x in range(start, end + 1):
            if target_int % cand_x == 0:
                cand_y = target_int // cand_x
                if cand_x > cand_y:
                    continue  # Ensure cand_x <= cand_y
                # Check closeness to approximates (prioritizes balance near sqrt)
                diff = abs(cand_x - approx_x) + abs(cand_y - approx_y)
                if diff < min_diff:
                    min_diff = diff
                    best_pair = (cand_x, cand_y)
        
        # Fallback: Find the most balanced factors overall (neither too low)
        # Prioritize pairs where x and y are closest (minimal ratio or difference)
        if best_pair is None:
            min_ratio = float('inf')
            for i in range(1, int(math.sqrt(target_int)) + 1):
                if target_int % i == 0:
                    j = target_int // i
                    if i <= j:
                        ratio = j / i if i > 0 else float('inf')
                        if ratio < min_ratio:
                            min_ratio = ratio
                            best_pair = (i, j)
        
        return best_pair
    
    def solve(self, equation, steps=100000, prefer_integers=False):
        print(f"\n[Physics Engine] Target Equation: {equation}")
        
        lhs_str, rhs_str = equation.split('=')
        
        # 1. Parse Target Safely
        try:
            target_val = float(eval(rhs_str))
            # Check if integer
            target_int = int(target_val) if target_val.is_integer() else None
        except (OverflowError, ValueError):
            target_val = float('inf')
            target_int = None
            print("Warning: Target is infinite or invalid.")
        
        if target_val == float('inf'):
            print("[System] Target too large for 64-bit float. Stopping.")
            return {}

        # Work in Log10 Space
        if target_val > 0:
            log_target = math.log10(target_val)
        else:
            log_target = -100
            
        print(f"[System] Target Magnitude: 10^{log_target:.2f}")
        
        if target_int is not None:
            print(f"[System] Target is integer: {target_int}")
            
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
        
        # Get floating-point results
        float_res = {n: d.val for n, d in self.variables.items()}
        
        # If preferring integers and simple x * y = N
        if prefer_integers and target_int and len(tokens) == 2:
            # Assume tokens are x and y
            if 'x' in tokens and 'y' in tokens:
                approx_x = float_res['x']
                approx_y = float_res['y']
                int_pair = self._find_integer_factors(target_int, approx_x, approx_y)
                if int_pair:
                    # Assign based on approximations for consistency (x closer to approx_x)
                    if abs(int_pair[0] - approx_x) < abs(int_pair[1] - approx_x):
                        float_res['x'] = int_pair[0]
                        float_res['y'] = int_pair[1]
                    else:
                        float_res['x'] = int_pair[1]
                        float_res['y'] = int_pair[0]
                    print(f"[Integer Mode] Found balanced factors: {int_pair[0]} * {int_pair[1]} = {target_int} (neither low, ratio ~{max(int_pair)/min(int_pair):.2f})")
        
        return float_res

# ==========================================
# 3. ASTRONOMICAL DEMONSTRATION
# ==========================================

if __name__ == "__main__":
    solver = AstroPhysicsSolver()

    # TEST: Multi-variable factorization, preferring integers
    res = solver.solve("x * y = 6666666666666666", prefer_integers=True)
    if 'x' in res and 'y' in res:
        print(f"\nResult x: {res['x']}")
        print(f"Result y: {res['y']}")
        print(f"Product:  {res['x'] * res['y']}")
