import qiskit
from qiskit import qasm2

c = qiskit.QuantumCircuit(1)
c.h(0)

# FIX: QuantumCircuit.qasm() was removed in Qiskit 1.0 -> use qasm2.dumps(c), because qasm2.dumps exports a circuit to an OpenQASM 2.0 string
qasm_str = qasm2.dumps(c)
print(qasm_str)
