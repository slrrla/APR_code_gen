import qiskit
import qiskit.qasm2

c = qiskit.QuantumCircuit(1)
c.h(0)

qasm_str = qiskit.qasm2.dumps(c)
print(qasm_str)
