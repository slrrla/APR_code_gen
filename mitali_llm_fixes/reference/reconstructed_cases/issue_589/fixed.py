import numpy as np
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, Aer, execute

def run_experiment(a1, a2, b1, b2, shots=1024):
    """Construct swap test circuit and measure.

    The swap circuit is quite simple:

    |0> --- H --- o --- H --- Measure
                  |
    a1 ---------- x ---------
                  |
    a2 ---------- x ---------

    (and identically for the second pair b1, b2 with its own ancilla)
    """
    ab = QuantumRegister(2, 'ab')
    cd = QuantumRegister(2, 'cd')
    anc = QuantumRegister(2, 'anc')
    cr = ClassicalRegister(2, 'c')
    qc = QuantumCircuit(ab, cd, anc, cr)

    qc.ry(2 * np.arcsin(a1), ab[0])
    qc.ry(2 * np.arcsin(a2), ab[1])
    qc.ry(2 * np.arcsin(b1), cd[0])
    qc.ry(2 * np.arcsin(b2), cd[1])

    qc.h(anc[0])
    qc.h(anc[1])
    qc.cswap(anc[0], ab[0], ab[1])
    qc.cswap(anc[1], cd[0], cd[1])
    qc.h(anc[0])
    qc.h(anc[1])

    qc.measure(anc[0], cr[0])
    qc.measure(anc[1], cr[1])

    simulator = Aer.get_backend('qasm_simulator')
    result = execute(qc, simulator, shots=shots).result()
    counts = result.get_counts()

    p0_ab = sum(c for bits, c in counts.items() if bits[-1] == '0') / shots
    p0_cd = sum(c for bits, c in counts.items() if bits[0] == '0') / shots

    print(f'a1: {a1:.3f} a1: {a2:.3f} b1: {b1:.3f} b2: {b2:.3f}')
    print(f'p0_ab: {p0_ab:.2f} p0_cd: {p0_cd:.2f} ')
    return p0_ab, p0_cd

def is_rectangle(A: int, B: int, C: int, D: int) -> int:
    max_val = float(max(A, B, C, D))
    p0_ab, p0_cd = run_experiment(A / max_val, B / max_val, C / max_val, D / max_val)
    return 1 if p0_ab > 0.99 and p0_cd > 0.99 else 0

if __name__ == "__main__":
    run_experiment(1.0, 1.0, 0.5, 0.5)
    run_experiment(0.5, 0.6, 0.2, 0.6)
