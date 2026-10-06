from qiskit import QuantumCircuit
from qiskit.circuit.library import C3XGate, C4XGate

sub = QuantumCircuit(16)
sub.cx(12, 4)
sub.ccx(12, 4, 5)
sub.append(C3XGate(), [4, 12, 5, 6])
sub.append(C4XGate(), [4, 12, 5, 6, 7])
sub.cx(13, 5)
sub.ccx(13, 5, 6)
sub.append(C3XGate(), [13, 5, 6, 7])
sub.cx(14, 6)
sub.ccx(14, 6, 7)
sub.cx(15, 7)

print("Sub circuit has", sub.num_qubits, "qubits")
print("Qubits in use:", sub.qubits)

csub = sub.control(1)
print("Controlled sub circuit has", csub.num_qubits, "qubits")
