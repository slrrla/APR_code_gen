# FIX: The QASM 2 exporter was not explicitly imported -> import qiskit.qasm2, because it provides the supported serialization API.
import qiskit.qasm2

c = qiskit.QuantumCircuit(1)
c.h(0)

# FIX: QuantumCircuit.qasm() was removed -> use qiskit.qasm2.dumps(c), because it returns the circuit as an OpenQASM 2.0 string.
qasm_str = qiskit.qasm2.dumps(c)
print(qasm_str)
