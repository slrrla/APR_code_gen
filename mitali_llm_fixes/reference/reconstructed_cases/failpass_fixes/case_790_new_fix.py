import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.quantum_info import SparsePauliOp
from qiskit.synthesis import SuzukiTrotter

N_qubit = 4
U = 1.0
J = 1.0
t = 1.0
h = [1.0] * N_qubit

H = SparsePauliOp.from_list([
    ("ZZII", U), ("IZZI", U), ("IIZZ", U),
    ("XXII", -J), ("IXXI", -J), ("IIXX", -J),
    ("YYII", -J), ("IYYI", -J), ("IIYY", -J),
    ("ZIII", h[0]), ("IZII", h[1]), ("IIZI", h[2]), ("IIIZ", h[3])
])

gate = PauliEvolutionGate(H, time=t)
st = SuzukiTrotter(order=2, reps=6)
circ = st.synthesize(gate)
print(circ)
