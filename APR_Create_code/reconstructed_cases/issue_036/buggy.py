import qiskit

c = qiskit.QuantumCircuit(1)
c.h(0)

qasm_str = c.qasm()
print(qasm_str)
