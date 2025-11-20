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
        if self.val < 1e-100:
            self.val = 1e-100

# ==========================================
# 2. LOG-SCALE MATH ENGINE
# ==========================================

class AstroPhysicsSolver:
    def __init__(self):
        self.variables = {}
        
    def create_var(self, name, rough_magnitude):
        self.variables[name] = AstroDomain(name, initial_scale=rough_magnitude)
    
    def _find_integer_factors(self, target_int, approx_x, approx_y, search_radius=100000000):
        """
        For integer targets and simple x * y = N equations, find exact integer factors
        close to the approximate floating-point solutions, prioritizing balance.
        Assumes two variables x and y, with x <= y. Enhanced for larger scans.
        """
        if target_int <= 0:
            return None
        
        # Ensure approx_x <= approx_y for consistency
        if approx_x > approx_y:
            approx_x, approx_y = approx_y, approx_x
        
        best_pair = None
        min_diff = float('inf')
        
        sqrt_n = math.isqrt(target_int)  # exact integer sqrt floor [web:65]
        
        # Enhanced Local search: Larger radius for bigger numbers, but cap checks for feasibility
        max_checks = 10000000  # Feasible limit: 10M checks
        start = max(1, int(approx_x) - search_radius)
        end = min(int(approx_x) + search_radius, sqrt_n)
        
        # Prioritize downward from approx_x (towards balance)
        direction = -1 if approx_x > sqrt_n / 2 else 1
        step_range = range(end, start - 1, direction)
        checked = 0
        for cand_x in step_range:
            if checked > max_checks:
                break
            if cand_x <= 0:
                continue
            if target_int % cand_x == 0:
                cand_y = target_int // cand_x
                if cand_x <= cand_y:
                    diff = abs(cand_x - approx_x) + abs(cand_y - approx_y)
                    if diff < min_diff:
                        min_diff = diff
                        best_pair = (cand_x, cand_y)
            checked += 1
        
        # Enhanced Fallback: Scan near sqrt(N) for balance
        if best_pair is None and sqrt_n > 1:
            fallback_start = sqrt_n
            fallback_end = max(1, sqrt_n - max_checks)
            fallback_checked = 0
            for i in range(fallback_start, fallback_end - 1, -1):
                if fallback_checked > max_checks:
                    break
                if target_int % i == 0:
                    j = target_int // i
                    if i <= j:
                        best_pair = (i, j)
                        break
                fallback_checked += 1
        
        # Ultimate Fallback: avoid trivial 1*N for large N; use approx sqrt if no factors found
        if best_pair is None:
            print("[Fallback] No non-trivial integer factors found in search region.")
            sqrt_approx = math.isqrt(target_int)  # integer floor sqrt [web:65]
            return (sqrt_approx, target_int // sqrt_approx)
        
        # If we only got 1 * N, report it but still return
        if best_pair[0] == 1 and target_int > 1:
            print("[Warning] Only trivial factors (1, N) found. N is prime or semiprime in this range.")
        
        return best_pair
    
    def solve(self, equation, steps=10000000, prefer_integers=False):
        print(f"\n[Physics Engine] Target Equation: {equation}")
        
        lhs_str, rhs_str = equation.split('=')
        
        # 1. Parse Target Safely - Handle large integers exactly
        target_int = None
        target_val = None
        try:
            rhs_stripped = rhs_str.strip()
            if 'e' in rhs_stripped.lower() or '.' in rhs_stripped:
                # Scientific or float
                target_val = float(eval(rhs_stripped))
                if target_val.is_integer():
                    target_int = int(target_val)
            else:
                # Assume integer literal
                target_int = int(rhs_stripped)
                target_val = float(target_int)
        except (ValueError, OverflowError):
            try:
                target_val = float(eval(rhs_stripped))
                if target_val.is_integer():
                    target_int = int(target_val)
            except Exception:
                target_val = float('inf')
                target_int = None
            print("Warning: Target parsing issues, using approximate.")
        
        if target_val is None or target_val == float('inf'):
            print("[System] Target too large or invalid. Stopping.")
            return {}

        # Work in Log10 Space
        if target_val > 0:
            log_target = math.log10(target_val)
        else:
            log_target = -100
            
        print(f"[System] Target Magnitude: 10^{log_target:.2f}")
        
        if target_int is not None:
            print(f"[System] Target is exact integer: {target_int}")
        else:
            print(f"[System] Target approximate: {target_val}")
            
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
        for _ in range(steps):
            vals = {n: d.val for n, d in self.variables.items()}
            
            # Evaluate LHS
            try:
                current_lhs = eval(lhs_str, {}, vals)
            except OverflowError:
                current_lhs = float('inf')
            
            # Current Log Magnitude
            if current_lhs <= 0:
                current_lhs = 1e-100
            try:
                log_current = math.log10(current_lhs)
            except ValueError:
                log_current = -100
                
            # ERROR: Difference in Orders of Magnitude
            error = log_current - log_target
            
            # Exit condition (precision on exponent)
            if abs(error) < 1e-8:
                break
                
            # 4. Sensitivity Analysis (Gradient Free)
            perturbation = 1.00001
            log_perturb_delta = math.log10(perturbation)
            
            for name in tokens:
                domain = self.variables[name]
                orig = domain.val
                
                # Test perturbation
                domain.val = orig * perturbation
                
                vals_new = {n: v.val for n, v in self.variables.items()}
                try:
                    lhs_new = eval(lhs_str, {}, vals_new)
                    if lhs_new <= 0:
                        lhs_new = 1e-100
                    log_new = math.log10(lhs_new)
                except Exception:
                    log_new = log_current
                
                # Sensitivity in log-log space
                sensitivity = (log_new - log_current) / log_perturb_delta
                domain.val = orig
                
                if abs(sensitivity) < 0.001:
                    sensitivity = 1.0
                
                force = -error / sensitivity
                force *= 50.0  # gain
                domain.update_multiplicative(force, dt=0.001)
        
        # Get floating-point results
        float_res = {n: d.val for n, d in self.variables.items()}
        
        # If preferring integers and simple x * y = N
        if prefer_integers and target_int is not None and len(tokens) == 2:
            if 'x' in tokens and 'y' in tokens:
                approx_x = float_res['x']
                approx_y = float_res['y']
                
                # Try to find exact integer factors near the float solution
                int_pair = self._find_integer_factors(target_int, approx_x, approx_y)
                if int_pair:
                    a, b = int_pair
                    # Order them so a <= b
                    if a > b:
                        a, b = b, a
                    float_res['x'] = a
                    float_res['y'] = b
                    print(f"[Integer Mode] Using integer pair: {a} * {b} = {a*b}")
                else:
                    # As a last resort, use isqrt-based balanced pair
                    s = math.isqrt(target_int)  # exact floor sqrt [web:65]
                    float_res['x'] = s
                    float_res['y'] = target_int // s
                    print(f"[Approx Integer Mode] Using isqrt-balanced pair: {s} * {target_int // s}")
        
        return float_res

# ==========================================
# 3. ASTRONOMICAL DEMONSTRATION
# ==========================================

if __name__ == "__main__":
    solver = AstroPhysicsSolver()

    # TEST: Multi-variable factorization, preferring integers
    res = solver.solve(
        "x * y = 170141183460469231731687303715884105727",
        prefer_integers=True
    )
    if 'x' in res and 'y' in res:
        print(f"\nResult x: {res['x']}")
        print(f"Result y: {res['y']}")
        print(f"Product:  {res['x'] * res['y']}")
