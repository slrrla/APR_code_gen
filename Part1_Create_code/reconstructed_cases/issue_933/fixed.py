from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library.standard_gates import RYGate
from qiskit.circuit import Parameter

qr = QuantumRegister(3)
circ = QuantumCircuit(qr)
a = Parameter('a')  # You can replace a with your choice of angle here
CCRY = RYGate(a).control(2)
circ.append(CCRY, qr)
print(circ)
