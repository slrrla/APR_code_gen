import numpy as np
from qiskit.circuit import Parameter
from qiskit.quantum_info import Pauli, SparsePauliOp
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.synthesis import SuzukiTrotter

J = Parameter("J")
h = Parameter("h")
N = 4

pauli_list = []
coeffs = []

for i in range(N - 1):
    x_p = np.zeros(N, dtype=bool)
    z_p = np.zeros(N, dtype=bool)
    z_p[i] = True
    z_p[i + 1] = True
    pauli_list.append(Pauli((z_p, x_p)))
    coeffs.append(-J)

for i in range(N):
    x_p = np.zeros(N, dtype=bool)
    z_p = np.zeros(N, dtype=bool)
    x_p[i] = True
    pauli_list.append(Pauli((z_p, x_p)))
    coeffs.append(h)

H = SparsePauliOp(pauli_list, coeffs=coeffs)

# assign J & h values:
H = H.assign_parameters({J: 1, h: 1})

gate = PauliEvolutionGate(H)

st = SuzukiTrotter(order=2, reps=6)
circ = st.synthesize(gate)
