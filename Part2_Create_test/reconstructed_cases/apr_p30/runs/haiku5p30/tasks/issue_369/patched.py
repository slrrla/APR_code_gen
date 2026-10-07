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

csub = sub.control(1)

i = 0
circ = QuantumCircuit(17)
# Fix: provide all 17 qubits for compose - control qubit i, then remaining qubits
# The controlled circuit has 17 qubits: qubit 0 is the control, qubits 1-16 are the original circuit
qubit_map = [i] + list(range(1, 17))
circ.compose(csub, qubit_map, inplace=True)
