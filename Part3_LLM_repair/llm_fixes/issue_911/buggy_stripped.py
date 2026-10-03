import qiskit
from qiskit.circuit.random import random_circuit

num_qubits = 3
depth = 1
max_operands = 2
qc = random_circuit(num_qubits, depth, max_operands=max_operands, seed=1)
qc = qc.decompose(reps=3)

for name_of_gate, qargs, cargs in qc.data:
    print("name of gate : ", name_of_gate)
    print("qargs : ", qargs, "\n")

    print("qargs[1] : ", qargs[1])
    print("qargs[1][1] : ", qargs[1][1])
    print("qargs[1].register : ", qargs[1].register)
    print("qargs[1].index : ", qargs[1].index)
