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

# FIX: the synthesis rule must be available when evolution gates are created -> initialize it before the loops, because it is assigned to each gate.
st = SuzukiTrotter(order=2, reps=6)

for j in range(0, N_qubit, 2):
    H = (U * Z ^ Z) - (J * X ^ X) - (J * Y ^ Y)
    # FIX: the evolution gate had no Suzuki-Trotter synthesis rule -> pass st to the gate, because synthesis operates on evolution gates.
    pauli_ev_gate = PauliEvolutionGate(H, time=t, synthesis=st)
    if j != N_qubit - 1:
        qc.append(pauli_ev_gate, [j, j + 1])

for j in range(1, N_qubit, 2):
    H = (U * Z ^ Z) - (J * X ^ X) - (J * Y ^ Y)
    # FIX: the evolution gate had no Suzuki-Trotter synthesis rule -> pass st to the gate, because synthesis operates on evolution gates.
    pauli_ev_gate = PauliEvolutionGate(H, time=t, synthesis=st)
    if j != N_qubit - 1:
        qc.append(pauli_ev_gate, [j, j + 1])

for j in range(N_qubit):
    # FIX: the evolution gate had no Suzuki-Trotter synthesis rule -> pass st to the gate, because synthesis operates on evolution gates.
    pauli_ev_gate = PauliEvolutionGate(h[j] * Z, time=t, synthesis=st)
    qc.append(pauli_ev_gate, [j])

# FIX: st.synthesize expects a PauliEvolutionGate, not a QuantumCircuit -> decompose the circuit, because each gate now carries the Suzuki-Trotter rule.
qc = qc.decompose()
