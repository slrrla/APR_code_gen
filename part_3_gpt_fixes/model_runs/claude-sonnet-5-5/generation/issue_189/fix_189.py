import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import GroverOperator
from qiskit.transpiler.passes import RemoveBarriers
from qiskit.converters import circuit_to_gate

oracle = QuantumCircuit(6)
oracle.z(5)
grover_operator = GroverOperator(oracle)
grover_operator = RemoveBarriers()(grover_operator)

n = 3
lg = 4
qpe = QuantumCircuit(n + lg + 2)

for i in range(n):
    Q = circuit_to_gate(grover_operator).control().power(2 ** ((n - 1) - i))
    j = i + 1
    # FIX: qubit list grew with each iteration (7, 8, 9 qubits) -> use one control qubit plus the fixed 6 target qubits, because the controlled gate always expects 7 qubits
    qp = [n - j] + list(np.arange(n, n + lg + 2))
    for l in range(len(qp)):
        print(qp[l])
    print(" ")
    qpe.append(Q, qp)
