import qiskit
from qiskit import Aer

# Use a local simulator backend which supports more than 1 qubit
backend = Aer.get_backend('qasm_simulator')

# Initialize two qubits and create Entanglement using Hadamard and CX/CNOT Gate
q = qiskit.QuantumRegister(2)
c = qiskit.ClassicalRegister(2)
qc = qiskit.QuantumCircuit(q, c)
qc.h(q[0])
qc.cx(q[0], q[1])
qc.measure(q, c)

job_exp = qiskit.execute(qc, backend=backend, shots=1024, max_credits=3)
