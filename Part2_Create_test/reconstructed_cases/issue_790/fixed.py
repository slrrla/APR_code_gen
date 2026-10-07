from qiskit.circuit.library import PauliEvolutionGate
from qiskit.quantum_info import SparsePauliOp
from qiskit.synthesis import SuzukiTrotter

N_qubit = 4
U = 1.0
J = 1.0
t = 1.0
h = [1.0] * N_qubit

labels = []
coefficients = []

for j in range(N_qubit - 1):
    for pauli, coefficient in (
        ("Z", U),
        ("X", -J),
        ("Y", -J),
    ):
        label = ["I"] * N_qubit
        label[j] = pauli
        label[j + 1] = pauli
        labels.append("".join(label))
        coefficients.append(coefficient)

for j in range(N_qubit):
    label = ["I"] * N_qubit
    label[j] = "Z"
    labels.append("".join(label))
    coefficients.append(h[j])

H = SparsePauliOp.from_list(list(zip(labels, coefficients)))

gate = PauliEvolutionGate(H, time=t)

st = SuzukiTrotter(order=2, reps=6)
qc = st.synthesize(gate)
