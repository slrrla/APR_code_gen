import qiskit
from qiskit.qasm2 import dumps

c = qiskit.QuantumCircuit(1)
c.h(0)

qasm_str = dumps(c)
print(qasm_str)
