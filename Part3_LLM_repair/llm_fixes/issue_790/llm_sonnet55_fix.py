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

# FIX: operators were plain Pauli objects, which can't be scaled by arbitrary coefficients or added/subtracted -> use SparsePauliOp, because it supports scalar multiplication, tensor and subtraction to build the Hamiltonian
X = SparsePauliOp("X")
Y = SparsePauliOp("Y")
Z = SparsePauliOp("Z")

qc = QuantumCircuit(N_qubit)

# FIX: SuzukiTrotter was created after the circuit was built and applied to a QuantumCircuit -> create it first and pass it to each gate via synthesis=, because the synthesizer works on PauliEvolutionGate, not on a circuit
st = SuzukiTrotter(order=2, reps=6)

for j in range(0, N_qubit, 2):
    H = (U * Z ^ Z) - (J * X ^ X) - (J * Y ^ Y)
    pauli_ev_gate = PauliEvolutionGate(H, time=t, synthesis=st)
    if j != N_qubit - 1:
        qc.append(pauli_ev_gate, [j, j + 1])

for j in range(1, N_qubit, 2):
    H = (U * Z ^ Z) - (J * X ^ X) - (J * Y ^ Y)
    pauli_ev_gate = PauliEvolutionGate(H, time=t, synthesis=st)
    if j != N_qubit - 1:
        qc.append(pauli_ev_gate, [j, j + 1])

for j in range(N_qubit):
    pauli_ev_gate = PauliEvolutionGate(h[j] * Z, time=t, synthesis=st)
    qc.append(pauli_ev_gate, [j])

# FIX: called st.synthesize(qc) on a QuantumCircuit (AttributeError) -> decompose the circuit, because decomposing expands each gate using its Suzuki-Trotter synthesis
qc = qc.decompose()
