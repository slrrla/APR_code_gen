import qiskit

c = qiskit.QuantumCircuit(1)
c.h(0)

# FIX: QuantumCircuit.qasm() was removed in Qiskit 1.0 -> use the OpenQASM 2 exporter, because qasm2.dumps() replaces the removed method
qasm_str = qiskit.qasm2.dumps(c)
print(qasm_str)
