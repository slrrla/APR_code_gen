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
    H = (U * Z ^ Z) - (J * X ^ X) - (J * Y ^ Y)
    pauli_ev_gate = PauliEvolutionGate(H, time=t)
    if j != N_qubit - 1:
        qc.append(pauli_ev_gate, [j, j + 1])

for j in range(1, N_qubit, 2):
    H = (U * Z ^ Z) - (J * X ^ X) - (J * Y ^ Y)
    pauli_ev_gate = PauliEvolutionGate(H, time=t)
    if j != N_qubit - 1:
        qc.append(pauli_ev_gate, [j, j + 1])

for j in range(N_qubit):
    pauli_ev_gate = PauliEvolutionGate(h[j] * Z, time=t)
    qc.append(pauli_ev_gate, [j])

st = SuzukiTrotter(order=2, reps=6)
# FIX: synthesize() was called on a QuantumCircuit (no .operator attribute) -> synthesize each PauliEvolutionGate and compose onto its qubits, because SuzukiTrotter.synthesize only accepts a PauliEvolutionGate
synth_qc = QuantumCircuit(N_qubit)
for inst in qc.data:
    synth_qc.compose(st.synthesize(inst.operation), [qc.find_bit(q).index for q in inst.qubits], inplace=True)
qc = synth_qc
