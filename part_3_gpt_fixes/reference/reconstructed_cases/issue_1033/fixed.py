import qiskit.quantum_info as qi
from qiskit.circuit import QuantumCircuit

# Two different constructions of a 3-qubit GHZ-like circuit
qc1 = QuantumCircuit(3)
qc1.h(0)
qc1.cx(0, 1)
qc1.cx(0, 2)
op1 = qi.Operator(qc1)
print(qc1)

qc2 = QuantumCircuit(3)
qc2.h(0)
qc2.cx(0, 1)
qc2.cx(1, 2)
op2 = qi.Operator(qc2)  # fixed: build the operator from qc2 to correctly compare the two circuits
print(qc2)

print(op1 == op2)
