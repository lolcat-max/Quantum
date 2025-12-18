# pip install qiskit qiskit-ibm-runtime scipy numpy

import sys
import time
from datetime import datetime, timezone

import numpy as np
from scipy.optimize import minimize

from qiskit.circuit.library import QAOAAnsatz
from qiskit.quantum_info import SparsePauliOp
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler


# -------------------- IBM account setup --------------------
# Run ONCE, then comment it out.
# IBM docs recommend save_account(...), then QiskitRuntimeService() loads it. [web:166]
QiskitRuntimeService.save_account(
    channel="ibm_quantum_platform",
    token="",
    set_as_default=True,
    overwrite=True,
)


# -------------------- countdown monitor --------------------
def _fmt_hhmmss(seconds):
    seconds = max(0, int(seconds))
    h, r = divmod(seconds, 3600)
    m, s = divmod(r, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

def monitor_job_countdown(job, label="job", poll_queue_every=20):
    t0 = time.time()
    last_queue_poll = 0.0
    est_done = None
    pos = None

    while True:
        status = job.status()
        now = datetime.now(timezone.utc)

        if (time.time() - last_queue_poll) >= poll_queue_every:
            last_queue_poll = time.time()
            try:
                qi = job.queue_info()  # may be None [web:193]
                if qi is not None:
                    est_done = getattr(qi, "estimated_completion_time", None) or getattr(qi, "estimated_end_time", None)
                    pos = getattr(qi, "position_in_queue", None) or getattr(qi, "position", None) or pos
            except Exception:
                pass
            try:
                pos2 = job.queue_position(refresh=True)  # may be None [web:137]
                if pos2 is not None:
                    pos = pos2
            except Exception:
                pass

        if est_done is not None:
            if est_done.tzinfo is None:
                est_done = est_done.replace(tzinfo=timezone.utc)
            remaining = (est_done - now).total_seconds()
            eta_text = f"ETA {_fmt_hhmmss(remaining)}"
        else:
            eta_text = f"elapsed {_fmt_hhmmss(time.time() - t0)}"

        sys.stdout.write("\r" + f"[{label}] {status} pos={pos} {eta_text}" + " " * 10)
        sys.stdout.flush()

        if str(status).upper() in {"DONE", "ERROR", "CANCELLED"}:
            sys.stdout.write("\n")
            sys.stdout.flush()
            return

        time.sleep(1)




# -------------------- factoring helpers --------------------
def bits_to_int(bits_msb_first):
    v = 0
    for b in bits_msb_first:
        v = (v << 1) | int(b)
    return v


def decode_pq(bitstring_msb_first, np_bits, nq_bits):
    bits = [int(c) for c in bitstring_msb_first]
    p = bits_to_int(bits[:np_bits])
    q = bits_to_int(bits[np_bits : np_bits + nq_bits])
    return p, q


def cost_from_bitstring_scaled(z, N, np_bits, nq_bits, force_odd=True):
    """
    Scaled cost so it stays numerically safe (float) in the optimizer. [web:80]
    """
    p, q = decode_pq(z, np_bits, nq_bits)
    if force_odd and ((p % 2 == 0) or (q % 2 == 0)):
        return 5.0
    err = p * q - N
    return float((err * err) / (N * N))


def diagonal_cost_op_walsh_small(N, np_bits, nq_bits, force_odd=True):
    """
    Small-n demo: build a Z-only SparsePauliOp from a diagonal energy table using
    a Walsh-Hadamard transform (only feasible for small n).
    """
    n = np_bits + nq_bits
    dim = 2**n

    energies = np.zeros(dim, dtype=float)
    for i in range(dim):
        z = format(i, f"0{n}b")  # MSB-first
        energies[i] = cost_from_bitstring_scaled(z, N, np_bits, nq_bits, force_odd)

    # Walsh-Hadamard transform
    c = energies.copy()
    h = 1
    while h < dim:
        for j in range(0, dim, 2 * h):
            for k in range(j, j + h):
                x, y = c[k], c[k + h]
                c[k], c[k + h] = x + y, x - y
        h *= 2
    c = c / dim

    paulis, coeffs = [], []
    for mask in range(dim):
        coeff = c[mask]
        if abs(coeff) < 1e-10:
            continue
        pstr = []
        for qb in range(n):
            bit = (mask >> (n - 1 - qb)) & 1
            pstr.append("Z" if bit else "I")
        paulis.append("".join(pstr))
        coeffs.append(coeff)

    return SparsePauliOp(paulis, coeffs=np.array(coeffs, dtype=complex))


def expected_cost_from_counts(counts, N, np_bits, nq_bits):
    shots = sum(counts.values())
    exp = 0.0
    for z, c in counts.items():
        exp += (c / shots) * cost_from_bitstring_scaled(z, N, np_bits, nq_bits, force_odd=True)
    return float(exp)


# -------------------- run on IBM hardware --------------------
def run_on_ibm_qpu(
    N=21,
    np_bits=3,
    nq_bits=3,
    reps=1,
    shots=2000,
    maxiter=10,
    poll_queue_every=15,
):
    """
    Submits QAOA circuits to a real IBM backend using SamplerV2. [web:99]
    Shows a live countdown when IBM provides estimated_completion_time. [web:156]
    """
    # Connect + pick backend
    service = QiskitRuntimeService()
    backend = service.least_busy(operational=True, simulator=False)
    print("Using backend:", backend.name)

    # Build QAOA circuit
    cost_op = diagonal_cost_op_walsh_small(N, np_bits, nq_bits, force_odd=True)
    ansatz = QAOAAnsatz(cost_operator=cost_op, reps=reps)
    ansatz.measure_all()

    # Transpile to backend ISA
    pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
    isa_ansatz = pm.run(ansatz)

    # Sampler
    sampler = Sampler(mode=backend)
    sampler.options.default_shots = shots

    # Objective executed on hardware
    def objective(theta):
        qc = isa_ansatz.assign_parameters(theta)
        job = sampler.run([qc])  # returns a RuntimeJob [web:99]
        monitor_job_countdown(job, label="objective", poll_queue_every=poll_queue_every)
        pub_result = job.result()[0]
        counts = pub_result.data.meas.get_counts()
        return expected_cost_from_counts(counts, N, np_bits, nq_bits)

    # Optimize
    x0 = np.random.default_rng(1).uniform(0, 2 * np.pi, size=len(isa_ansatz.parameters))
    res = minimize(objective, x0, method="COBYLA", options={"maxiter": maxiter})

    # Final sample
    qc_best = isa_ansatz.assign_parameters(res.x)
    job = sampler.run([qc_best])
    monitor_job_countdown(job, label="final", poll_queue_every=poll_queue_every)
    pub_result = job.result()[0]
    counts = pub_result.data.meas.get_counts()

    # Decode top outcomes
    top = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)[:10]
    decoded = []
    for z, c in top:
        p, q = decode_pq(z, np_bits, nq_bits)
        decoded.append((z, c, p, q, p * q))

    return backend.name, res, decoded, counts


if __name__ == "__main__":
    # Start small on hardware. (3+3 qubits is already nontrivial once transpiled.) [web:156]
    backend_name, res, decoded, counts = run_on_ibm_qpu(
        N=21,
        np_bits=3,
        nq_bits=3,
        reps=1,
        shots=2000,
        maxiter=1,
        poll_queue_every=20,
    )

    print("Backend:", backend_name)
    print("Optimization success:", res.success, "final objective:", res.fun)
    print("Top bitstrings (z, shots, p, q, p*q):")
    for row in decoded:
        print(row)
