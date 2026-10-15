import qiskit
# FIX: qiskit 1.0 removed QuantumCircuit.qasm(); the qasm2 module must be imported explicitly -> added `import qiskit.qasm2`, because qiskit.qasm2.dumps is the 1.0 replacement and needs that submodule loaded
import qiskit.qasm2

c = qiskit.QuantumCircuit(1)
c.h(0)

# FIX: c.qasm() no longer exists in qiskit 1.0 -> replaced with qiskit.qasm2.dumps(c), because it serializes the circuit to an OpenQASM 2.0 string
qasm_str = qiskit.qasm2.dumps(c)
print(qasm_str)
