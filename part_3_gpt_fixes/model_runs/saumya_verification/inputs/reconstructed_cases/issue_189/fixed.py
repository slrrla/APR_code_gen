import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import GroverOperator
from qiskit.transpiler.passes import RemoveBarriers
from qiskit.converters import circuit_to_gate

# Build a simple oracle/Grover operator on 6 qubits
oracle = QuantumCircuit(6)
oracle.z(5)
grover_operator = GroverOperator(oracle)
grover_operator = RemoveBarriers()(grover_operator)

n = 3
lg = 4
qpe = QuantumCircuit(n + lg + 2)

# FIX: qp is fixed length, computed once outside the loop; the control
# qubit index i is prepended so the total qubit count matches Q every time
qp = list(np.arange(n, n + lg + 2))
for i in range(n):
    Q = circuit_to_gate(grover_operator).control().power(2 ** ((n - 1) - i))
    qpe.append(Q, [i] + qp)
