import numpy as np
import math
import warnings
import sys
import random
import time
from decimal import Decimal, getcontext

# ==========================================
# CONFIGURATION
# ==========================================
try:
    sys.set_int_max_str_digits(0)
except AttributeError:
    pass

getcontext().prec = 500
sys.setrecursionlimit(5000)
warnings.filterwarnings("ignore")

# ==========================================
# 1. THE "UNDER 100" CHECKER
# ==========================================

def find_factor_under_100(n):
    """
    Scans for any factor 'p' where p < 100.
    Returns 'p' if found (meaning n is Composite).
    Returns None if no small factor exists.
    """
    # We iterate 2 through 99
    # Optimization: We only really need to check primes, but brute force 2..99 is fast enough
    for p in range(2, 100):
        if n % p == 0:
            return p
    return None

# ==========================================
# 2. PHYSICS SOLVER CLASS
# ==========================================

class AstroPhysicsSolver:
    def _miller_rabin_check(self, n, k=5):
        """Final confirmation step."""
        if n == 2 or n == 3: return True
        if n % 2 == 0 or n < 2: return False
        r, d = 0, n - 1
        while d % 2 == 0:
            r += 1
            d //= 2
        for _ in range(k):
            a = random.randint(2, n - 2)
            x = pow(a, d, n)
            if x == 1 or x == n - 1: continue
            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1: break
            else:
                return False
        return True

    def is_prime_candidate(self, target_int):
        """
        Returns True if the number is a valid Prime Candidate.
        Returns False if it fails the "p < 100" check or other tests.
        """
        # PHASE 1: THE "p < 100" BRUTE FORCE
        # If we find a p < 100, it is NOT a prime.
        small_p = find_factor_under_100(target_int)
        
        if small_p is not None:
            # Discard immediately
            return False, f"Failed (Divisible by {small_p})"
            
        # PHASE 2: DEEP CHECK (Miller-Rabin)
        # If it survived Phase 1, it has no small factors. 
        # Now we check if it is truly prime.
        if self._miller_rabin_check(target_int):
            return True, "PRIME CONFIRMED"
        else:
            return False, "Failed (Composite with large factors)"

# ==========================================
# 3. THE PRIME GENERATOR LOOP
# ==========================================

def generate_primes(start_num, count_needed=10):
    solver = AstroPhysicsSolver()
    
    print(f"\n[Prime Generator] Scanning from {str(start_num)[:15]}...")
    print(f"[Strategy] Discard if p (factor) < 100")
    print("-" * 75)
    print(f"{'OFFSET':<8} | {'RESULT':<30} | {'DETAILS'}")
    print("-" * 75)
    
    primes_found = []
    current = start_num
    if current % 2 == 0: current += 1 # Ensure odd start
    
    checked = 0
    
    while len(primes_found) < count_needed:
        is_prime, reason = solver.is_prime_candidate(current)
        
        if is_prime:
            print(f"{checked:<8} | ** PRIME DETECTED **           | {str(current)[:20]}...")
            primes_found.append(current)
        else:
            # Optional: Print failures to show the "Under 100" logic working
            # We limit print output to keep it readable
            if "Divisible by" in reason and checked < 10:
                 print(f"{checked:<8} | Discarded                      | {reason}")
        
        current += 2
        checked += 1
        
        # Safety break for demo
        if checked > 10000: 
            print("... Limit reached for demo ...")
            break
            
    return primes_found

# ==========================================
# DEMONSTRATION
# ==========================================

if __name__ == "__main__":
    # 1. Generate Primes starting at a massive number
    # 10^50 + 1
    EXPONENT = 500
    START = (10 ** EXPONENT) + 1
    
    found = generate_primes(START, count_needed=5)
    
    print("-" * 75)
    print(f"Found {len(found)} Primes.")
    print(f"Last Prime Found: {found[-1]}")
