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

# FIX: define the synthesis before constructing the evolution gates -> keep SuzukiTrotter available for each gate, because it synthesizes PauliEvolutionGate objects rather than whole circuits
st = SuzukiTrotter(order=2, reps=6)

qc = QuantumCircuit(N_qubit)

for j in range(0, N_qubit, 2):
    H = (U * Z ^ Z) - (J * X ^ X) - (J * Y ^ Y)
    # FIX: attach SuzukiTrotter to the evolution gate -> use the requested synthesis for this gate, because synthesize does not accept a QuantumCircuit
    pauli_ev_gate = PauliEvolutionGate(H, time=t, synthesis=st)
    if j != N_qubit - 1:
        qc.append(pauli_ev_gate, [j, j + 1])

for j in range(1, N_qubit, 2):
    H = (U * Z ^ Z) - (J * X ^ X) - (J * Y ^ Y)
    # FIX: attach SuzukiTrotter to the evolution gate -> use the requested synthesis for this gate, because synthesize does not accept a QuantumCircuit
    pauli_ev_gate = PauliEvolutionGate(H, time=t, synthesis=st)
    if j != N_qubit - 1:
        qc.append(pauli_ev_gate, [j, j + 1])

for j in range(N_qubit):
    # FIX: attach SuzukiTrotter to the evolution gate -> use the requested synthesis for this gate, because synthesize does not accept a QuantumCircuit
    pauli_ev_gate = PauliEvolutionGate(h[j] * Z, time=t, synthesis=st)
    qc.append(pauli_ev_gate, [j])

# FIX: decompose the circuit's evolution gates -> apply their attached SuzukiTrotter synthesis, because st.synthesize expects an evolution gate, not a circuit
qc = qc.decompose()
