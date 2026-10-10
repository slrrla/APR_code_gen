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

    # FIX: Single-qubit gates have no qargs[1], and Qubit lacks subscripting and public register/index attributes -> guard the second operand and use qc.find_bit, because it provides supported register and index lookup.
    if len(qargs) > 1:
        print("qargs[1] : ", qargs[1])
        print("qargs[1][1] : ", qc.find_bit(qargs[1]).registers[0][1])
        print("qargs[1].register : ", qc.find_bit(qargs[1]).registers[0][0])
        print("qargs[1].index : ", qc.find_bit(qargs[1]).index)

