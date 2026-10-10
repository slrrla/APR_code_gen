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

    # FIX: Qubit objects have no register or index attributes, and qargs[1] fails for single-qubit gates -> use find_bit on the last qarg, because it provides that bit's register and index.
    print("qargs[-1] : ", qargs[-1])
    print("register index : ", qc.find_bit(qargs[-1]).registers[0][1])
    print("register : ", qc.find_bit(qargs[-1]).registers[0][0])
    print("circuit index : ", qc.find_bit(qargs[-1]).index)
