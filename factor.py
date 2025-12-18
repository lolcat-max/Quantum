# pip install qiskit qiskit-ibm-runtime scipy numpy
from qiskit_ibm_runtime import QiskitRuntimeService

QiskitRuntimeService.save_account(
    channel="ibm_quantum_platform",
    token="API_KEY_HERE",
    set_as_default=True,
    overwrite=True,
)

service = QiskitRuntimeService()  # should work now
print(service.backends()[:3])
import numpy as np
from scipy.optimize import minimize

from qiskit.circuit.library import QAOAAnsatz
from qiskit.quantum_info import SparsePauliOp

from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

# ---------- helpers ----------
def bits_to_int(bits_msb_first):
    v = 0
    for b in bits_msb_first:
        v = (v << 1) | int(b)
    return v

def decode_pq(bitstring_msb_first, np_bits, nq_bits):
    bits = [int(c) for c in bitstring_msb_first]
    p = bits_to_int(bits[:np_bits])
    q = bits_to_int(bits[np_bits:np_bits+nq_bits])
    return p, q

def cost_from_bitstring_scaled(z, N, np_bits, nq_bits, force_odd=True):
    p, q = decode_pq(z, np_bits, nq_bits)
    if force_odd and ((p % 2 == 0) or (q % 2 == 0)):
        return 5.0  # constant penalty
    # scaled cost to avoid overflow and keep optimizer stable
    err = p*q - N
    return float((err*err) / (N*N))

def diagonal_cost_op_walsh_small(N, np_bits, nq_bits, force_odd=True):
    # Small-n demo: convert diagonal energies table -> Z-Pauli sum via Walsh-Hadamard.
    n = np_bits + nq_bits
    dim = 2**n

    energies = np.zeros(dim, dtype=float)
    for i in range(dim):
        z = format(i, f"0{n}b")  # MSB-first
        energies[i] = cost_from_bitstring_scaled(z, N, np_bits, nq_bits, force_odd)

    c = energies.copy()
    h = 1
    while h < dim:
        for j in range(0, dim, 2*h):
            for k in range(j, j+h):
                x, y = c[k], c[k+h]
                c[k], c[k+h] = x + y, x - y
        h *= 2
    c = c / dim

    paulis, coeffs = [], []
    for mask in range(dim):
        coeff = c[mask]
        if abs(coeff) < 1e-10:
            continue
        pstr = []
        for qb in range(n):
            bit = (mask >> (n-1-qb)) & 1
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

# ---------- main: run on IBM hardware ----------
def run_on_ibm_qpu(N=21, np_bits=3, nq_bits=3, reps=1, shots=2000, maxiter=25):
    n = np_bits + nq_bits
    cost_op = diagonal_cost_op_walsh_small(N, np_bits, nq_bits, force_odd=True)
    ansatz = QAOAAnsatz(cost_operator=cost_op, reps=reps)
    ansatz.measure_all()

    # 1) connect + pick a real backend
    service = QiskitRuntimeService()  # expects your IBM token is configured
    backend = service.least_busy(operational=True, simulator=False)  # real QPU [web:103]
    pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
    isa_ansatz = pm.run(ansatz)

    sampler = Sampler(mode=backend)
    sampler.options.default_shots = shots

    # objective uses hardware sampling
    def objective(theta):
        qc = isa_ansatz.assign_parameters(theta)
        job = sampler.run([qc])                 # submit to hardware [web:99]
        pub_result = job.result()[0]
        counts = pub_result.data.meas.get_counts()
        return expected_cost_from_counts(counts, N, np_bits, nq_bits)

    x0 = np.random.default_rng(1).uniform(0, 2*np.pi, size=len(isa_ansatz.parameters))
    res = minimize(objective, x0, method="COBYLA", options={"maxiter": maxiter})

    # final sample at best params
    qc_best = isa_ansatz.assign_parameters(res.x)
    job = sampler.run([qc_best])
    pub_result = job.result()[0]
    counts = pub_result.data.meas.get_counts()

    top = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)[:10]
    decoded = []
    for z, c in top:
        p, q = decode_pq(z, np_bits, nq_bits)
        decoded.append((z, c, p, q, p*q))

    return backend.name, res, decoded, counts

if __name__ == "__main__":
    backend_name, res, decoded, counts = run_on_ibm_qpu(N=21, np_bits=3, nq_bits=3, reps=1, shots=2000, maxiter=20)
    print("Backend:", backend_name)
    print("Optimization success:", res.success, "final objective:", res.fun)
    print("Top bitstrings (z, shots, p, q, p*q):")
    for row in decoded:
        print(row)
