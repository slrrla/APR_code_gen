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

# FIX: synthesis was attempted on the full QuantumCircuit -> create a Suzuki-Trotter synthesizer for individual evolution gates, because synthesize requires a PauliEvolutionGate
st = SuzukiTrotter(order=2, reps=6)

for j in range(0, N_qubit, 2):
    H = (U * Z ^ Z) - (J * X ^ X) - (J * Y ^ Y)
    pauli_ev_gate = PauliEvolutionGate(H, time=t)
    if j != N_qubit - 1:
        # FIX: the evolution gate was appended without Suzuki-Trotter synthesis -> synthesize it before composing it, because SuzukiTrotter operates on evolution gates
        qc.compose(st.synthesize(pauli_ev_gate), [j, j + 1], inplace=True)

for j in range(1, N_qubit, 2):
    H = (U * Z ^ Z) - (J * X ^ X) - (J * Y ^ Y)
    pauli_ev_gate = PauliEvolutionGate(H, time=t)
    if j != N_qubit - 1:
        # FIX: the evolution gate was appended without Suzuki-Trotter synthesis -> synthesize it before composing it, because SuzukiTrotter operates on evolution gates
        qc.compose(st.synthesize(pauli_ev_gate), [j, j + 1], inplace=True)

for j in range(N_qubit):
    pauli_ev_gate = PauliEvolutionGate(h[j] * Z, time=t)
    # FIX: the single-qubit evolution gate was appended without Suzuki-Trotter synthesis -> synthesize it before composing it, because SuzukiTrotter operates on evolution gates
    qc.compose(st.synthesize(pauli_ev_gate), [j], inplace=True)
