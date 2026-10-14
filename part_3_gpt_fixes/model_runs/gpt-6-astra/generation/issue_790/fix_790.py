import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.quantum_info import Pauli, SparsePauliOp
from qiskit.synthesis import SuzukiTrotter

N_qubit = 4
U = 1.0
J = 1.0
t = 1.0
h = [1.0] * N_qubit

X = Pauli("X")
Y = Pauli("Y")
Z = Pauli("Z")

qc = QuantumCircuit(N_qubit)

for j in range(0, N_qubit, 2):
    # FIX: Pauli objects do not support weighted sums -> use SparsePauliOp, because it represents the intended two-qubit Hamiltonian.
    H = SparsePauliOp(["ZZ", "XX", "YY"], coeffs=[U, -J, -J])
    pauli_ev_gate = PauliEvolutionGate(H, time=t)
    if j != N_qubit - 1:
        qc.append(pauli_ev_gate, [j, j + 1])

for j in range(1, N_qubit, 2):
    # FIX: Pauli objects do not support weighted sums -> use SparsePauliOp, because it represents the intended two-qubit Hamiltonian.
    H = SparsePauliOp(["ZZ", "XX", "YY"], coeffs=[U, -J, -J])
    pauli_ev_gate = PauliEvolutionGate(H, time=t)
    if j != N_qubit - 1:
        qc.append(pauli_ev_gate, [j, j + 1])

for j in range(N_qubit):
    # FIX: Pauli does not support arbitrary scalar coefficients -> use SparsePauliOp, because it preserves the field strength h[j].
    pauli_ev_gate = PauliEvolutionGate(SparsePauliOp(Z, coeffs=[h[j]]), time=t)
    qc.append(pauli_ev_gate, [j])

st = SuzukiTrotter(order=2, reps=6)
# FIX: synthesize expects a PauliEvolutionGate, not a QuantumCircuit -> configure each evolution gate and decompose, because this applies Suzuki-Trotter synthesis while preserving the circuit's gate order.
for instruction in qc.data:
    instruction.operation.synthesis = st
qc = qc.decompose()
