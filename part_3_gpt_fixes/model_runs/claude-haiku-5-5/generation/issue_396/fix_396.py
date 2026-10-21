from qiskit.quantum_info import Statevector
from qiskit import QuantumCircuit
from qiskit.circuit.library import GroverOperator, Diagonal

targets = ['101', '110']

# FIX: Statevector.from_label cannot take a list and builds a basis state rather than a phase oracle -> build a 3-qubit circuit with a Diagonal gate that sets phase -1 on each target index, because GroverOperator needs a phase-oracle circuit
diag = [1] * 8
for t in targets:
    diag[int(t, 2)] = -1
oracle = QuantumCircuit(3)
oracle.append(Diagonal(diag), [0, 1, 2])

grover_op = GroverOperator(oracle)
print(grover_op)
