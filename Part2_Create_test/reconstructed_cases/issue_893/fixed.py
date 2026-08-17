from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

state = Statevector.from_label("+-rl")

qc = QuantumCircuit(4)
qc.prepare_state(state, [0, 1, 2, 3])

print(qc)
