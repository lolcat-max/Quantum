import math
import warnings
import sys
import random

sys.setrecursionlimit(2000)
warnings.filterwarnings("ignore")

# ==========================================
# 1. INTEGER-BASED PHYSICS KERNEL
# ==========================================

class AstroDomain:
    def __init__(self, name, initial_scale=10):
        self.name = name
        # Integer-based value with fixed-point precision (scale by 10^18 for sub-integer precision)
        self.val = initial_scale
        self.velocity = 0
        self.scale = 10**18  # Fixed-point precision multiplier
        
    def update_multiplicative(self, force_int, dt_scaled):
        """
        Integer-only multiplicative update using fixed-point arithmetic.
        val_new = val_old * (1 + velocity * dt)
        All operations in integer domain with scaling.
        """
        # Damping: velocity = 0.8*velocity + 0.2*force (scaled by 10^18)
        self.velocity = (self.velocity * 8 + force_int * 2) // 10
        
        # Cap velocity: -0.1 to +0.1 (scaled: -10^17 to +10^17)
        max_velocity = self.scale // 10  # 0.1 scaled
        if self.velocity > max_velocity:
            self.velocity = max_velocity
        elif self.velocity < -max_velocity:
            self.velocity = -max_velocity
        
        # Apply: val = val * (1 + velocity * dt)
        # dt_scaled is dt * 10^18, velocity is scaled
        step_change = (self.velocity * dt_scaled) // (self.scale * self.scale)
        
        # val = val + val * step_change / scale
        delta = (self.val * step_change) // self.scale
        self.val += delta
        
        # Safety floor
        if self.val < 1:
            self.val = 1

# ==========================================
# PRIME VALIDATION (Integer-Based Miller-Rabin)
# ==========================================

def is_prime_miller_rabin(n, k=40):
    """
    Integer-only Miller-Rabin primality test.
    """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    
    # Write n-1 as 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    
    # Deterministic witnesses for n < 2^64
    if n < 2**64:
        witnesses = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    else:
        witnesses = [random.randrange(2, min(n - 2, 2**64)) for _ in range(k)]
    
    for a in witnesses:
        if a >= n:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

# ==========================================
# 2. INTEGER-BASED LOG-SCALE MATH ENGINE
# ==========================================

class AstroPhysicsSolver:
    def __init__(self):
        self.variables = {}
        
    def create_var(self, name, rough_magnitude):
        self.variables[name] = AstroDomain(name, initial_scale=rough_magnitude)
    
    def _integer_log10(self, n):
        """Calculate log10 using integer arithmetic (returns scaled by 10^18)"""
        if n <= 0:
            return -100 * (10**18)
        
        # Use bit_length for fast approximation: log10(n) ≈ bit_length * log10(2)
        # log10(2) ≈ 0.30102999566 ≈ 301029995664 / 10^12
        bit_len = n.bit_length()
        return (bit_len * 301029995664 * (10**6)) // (10**12)
    
    def _integer_pow10(self, log_val_scaled):
        """Calculate 10^x using integer arithmetic (log_val_scaled is scaled by 10^18)"""
        # For initialization only - returns integer approximation
        exponent = log_val_scaled // (10**18)
        if exponent > 1000:
            # Too large, use bit approximation
            # 10^x ≈ 2^(x * log2(10)) where log2(10) ≈ 3.32192809489
            bits = (exponent * 3321928094) // (10**9)
            return 1 << min(bits, 10000)  # Cap to prevent overflow
        return 10 ** exponent
    
    def _find_integer_factors(self, target_int, approx_x, approx_y, search_radius=1000000):
        """
        Integer-only factor search with prime validation.
        """
        if target_int <= 0:
            return None
        
        # Ensure approx_x <= approx_y
        if approx_x > approx_y:
            approx_x, approx_y = approx_y, approx_x
        
        best_pair = None
        min_diff = 2**256  # Large integer
        
        # Integer square root
        sqrt_n = math.isqrt(target_int)
        
        print(f"[Integer Brute Force] Searching near sqrt(N) = {sqrt_n}")
        
        # Local search near approximations
        start = max(2, approx_x - search_radius)
        end = min(approx_x + search_radius, sqrt_n)
        
        checked = 0
        for cand_x in range(end, start - 1, -1):
            checked += 1
            if checked > 1000000:  # Limit checks
                break
                
            if target_int % cand_x == 0:
                cand_y = target_int // cand_x
                if cand_x <= cand_y:
                    print(f"[Integer Check] Testing: {cand_x} * {cand_y}")
                    if is_prime_miller_rabin(cand_x) and is_prime_miller_rabin(cand_y):
                        diff = abs(cand_x - approx_x) + abs(cand_y - approx_y)
                        if diff < min_diff:
                            min_diff = diff
                            best_pair = (cand_x, cand_y)
                            print(f"[✓ Prime Factors] {cand_x} * {cand_y} = {target_int}")
                            break
        
        # Fallback: scan near sqrt
        if best_pair is None:
            print(f"[Integer Fallback] Scanning from sqrt...")
            for i in range(sqrt_n, max(2, sqrt_n - 1000000), -1):
                if target_int % i == 0:
                    j = target_int // i
                    if is_prime_miller_rabin(i) and is_prime_miller_rabin(j):
                        best_pair = (i, j)
                        print(f"[✓ Prime Factors] {i} * {j} = {target_int}")
                        break
        
        # Small prime trial
        if best_pair is None:
            print(f"[Integer Small Prime] Trying small factors...")
            for i in range(2, min(100000, sqrt_n + 1)):
                if target_int % i == 0:
                    j = target_int // i
                    if is_prime_miller_rabin(i) and is_prime_miller_rabin(j):
                        best_pair = (i, j)
                        print(f"[✓ Small Prime] {i} * {j} = {target_int}")
                        break
        
        if best_pair is None:
            print(f"[✗ No Prime Factors] Requires advanced factorization")
        
        return best_pair
    
    def solve(self, equation, steps=1000000, prefer_integers=False):
        print(f"\n[Integer Physics Engine] Target: {equation}")
        
        lhs_str, rhs_str = equation.split('=')
        
        # Parse target as integer
        target_int = int(rhs_str.strip())
        print(f"[System] Target integer: {target_int}")
        print(f"[System] Bit length: {target_int.bit_length()} bits")
        
        # Integer log10 (scaled by 10^18)
        log_target_scaled = self._integer_log10(target_int)
        
        # Initialize variables
        import re
        tokens = list(set(re.findall(r'[a-zA-Z_]+', lhs_str)))
        num_vars = len(tokens) if len(tokens) > 0 else 1
        
        # Initial magnitude (integer)
        sqrt_target = math.isqrt(target_int)
        estimated_scale = math.isqrt(sqrt_target) if num_vars > 1 else sqrt_target
        
        for t in tokens:
            if t not in self.variables:
                self.create_var(t, rough_magnitude=max(2, estimated_scale))
        
        scale = 10**18
        
        # Integer annealing loop
        for iteration in range(steps):
            vals = {n: d.val for n, d in self.variables.items()}
            
            # Evaluate LHS (pure integer multiplication)
            current_lhs = 1
            for token in tokens:
                current_lhs *= vals[token]
            
            # Integer log of current
            log_current_scaled = self._integer_log10(current_lhs)
            
            # Error (scaled integer)
            error_scaled = log_current_scaled - log_target_scaled
            
            # Exit if converged (error < 1e-8 scaled)
            if abs(error_scaled) < (scale // 100000000):
                break
            
            # Sensitivity analysis (integer-based)
            # Perturbation: 1.001 = 1 + 1/1000
            for name in tokens:
                domain = self.variables[name]
                orig = domain.val
                
                # Perturb: val * 1.001 = val + val/1000
                domain.val = orig + max(1, orig // 1000)
                
                vals_new = {n: d.val for n, d in self.variables.items()}
                lhs_new = 1
                for token in tokens:
                    lhs_new *= vals_new[token]
                
                log_new_scaled = self._integer_log10(lhs_new)
                domain.val = orig
                
                # Sensitivity (scaled integer)
                log_delta = self._integer_log10(1001) - self._integer_log10(1000)
                if log_delta == 0:
                    log_delta = 1
                    
                sensitivity_scaled = (log_new_scaled - log_current_scaled) * scale // log_delta
                
                if abs(sensitivity_scaled) < scale // 1000:
                    sensitivity_scaled = scale
                
                # Force (scaled integer)
                force_scaled = -(error_scaled * scale) // sensitivity_scaled
                force_scaled = (force_scaled * 10 * scale) // scale  # Multiply by 10
                
                # Update with integer arithmetic
                dt_scaled = scale // 100  # dt = 0.01
                domain.update_multiplicative(force_scaled, dt_scaled)
        
        # Get integer results
        int_res = {n: d.val for n, d in self.variables.items()}
        
        # Factor search
        if prefer_integers and len(tokens) == 2:
            if 'x' in tokens and 'y' in tokens:
                approx_x = int_res['x']
                approx_y = int_res['y']
                int_pair = self._find_integer_factors(target_int, approx_x, approx_y)
                
                if int_pair:
                    pair_small, pair_large = min(int_pair), max(int_pair)
                    bits_p = pair_small.bit_length()
                    bits_q = pair_large.bit_length()
                    total_bits = target_int.bit_length()
                    ratio = bits_p / total_bits
                    is_brilliant = 0.4 <= ratio <= 0.6
                    
                    int_res['x'] = pair_small
                    int_res['y'] = pair_large
                    print(f"[Integer Result] {pair_small} * {pair_large} = {target_int}")
                    print(f"[Brilliant] Ratio: {ratio:.2f} - {'✓ VALID' if is_brilliant else '✗ UNBALANCED'}")
                else:
                    print(f"[Warning] No factorization - use ECM/NFS")
        
        return int_res

# ==========================================
# 3. DEMONSTRATION
# ==========================================

if __name__ == "__main__":
    solver = AstroPhysicsSolver()

    res = solver.solve("x * y = 1270342900999153747446613209254773222471869972643795821950924914273158308998256153239605448614337959340089858661901149616213942560503075430046535667274537340778628434242609437044787311110308726228793510821924124288335353430696923751", prefer_integers=True)
    if 'x' in res and 'y' in res:
        print(f"\nResult x: {res['x']}")
        print(f"Result y: {res['y']}")
        print(f"Product:  {res['x'] * res['y']}")
