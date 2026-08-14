import qiskit as qk
from qiskit.quantum_info import random_clifford
from qiskit.quantum_info import Clifford

qc = qk.QuantumCircuit(3)
U = random_clifford(3, seed=123)
U = Clifford.to_circuit(U)
qc.compose(U, qubits=[0, 1, 2])
qc.draw("mpl")
