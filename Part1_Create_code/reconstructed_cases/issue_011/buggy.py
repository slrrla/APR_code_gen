from qiskit import QuantumCircuit
from qiskit.circuit.library import QFT

N = 21
work_qubits = 3
control_qubits = 2

qc = QuantumCircuit(control_qubits + work_qubits, control_qubits)
qc.h(range(control_qubits))
qc.x(control_qubits)

qc.append(QFT(control_qubits, inverse=True), range(control_qubits))
qc.measure(range(control_qubits), range(control_qubits))

print(N, control_qubits, work_qubits, qc.num_qubits)
