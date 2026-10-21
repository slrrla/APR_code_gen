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

# FIX: SuzukiTrotter was created after the circuit was built and only used via synthesize() on a QuantumCircuit -> create it up front and pass it as the synthesis of each PauliEvolutionGate, because synthesis must be attached to evolution gates, not circuits
st = SuzukiTrotter(order=2, reps=6)

for j in range(0, N_qubit, 2):
    H = (U * Z ^ Z) - (J * X ^ X) - (J * Y ^ Y)
    # FIX: added synthesis=st so this evolution gate is Suzuki-Trotter synthesized -> attached the synthesis to the gate, because PauliEvolutionGate uses its synthesis when decomposed
    pauli_ev_gate = PauliEvolutionGate(H, time=t, synthesis=st)
    if j != N_qubit - 1:
        qc.append(pauli_ev_gate, [j, j + 1])

for j in range(1, N_qubit, 2):
    H = (U * Z ^ Z) - (J * X ^ X) - (J * Y ^ Y)
    # FIX: added synthesis=st so this evolution gate is Suzuki-Trotter synthesized -> attached the synthesis to the gate, because PauliEvolutionGate uses its synthesis when decomposed
    pauli_ev_gate = PauliEvolutionGate(H, time=t, synthesis=st)
    if j != N_qubit - 1:
        qc.append(pauli_ev_gate, [j, j + 1])

for j in range(N_qubit):
    # FIX: added synthesis=st so this single-qubit evolution gate is Suzuki-Trotter synthesized -> attached the synthesis to the gate, because PauliEvolutionGate uses its synthesis when decomposed
    pauli_ev_gate = PauliEvolutionGate(h[j] * Z, time=t, synthesis=st)
    qc.append(pauli_ev_gate, [j])

# FIX: st.synthesize(qc) raised AttributeError (no .operator on QuantumCircuit) -> decompose the circuit so each attached SuzukiTrotter synthesis is expanded, because decompose() on PauliEvolutionGate uses its synthesis
qc = qc.decompose()
