import qiskit
from qiskit import qasm2

c = qiskit.QuantumCircuit(1)
c.h(0)

qasm_str = qasm2.dumps(c)
print(qasm_str)
