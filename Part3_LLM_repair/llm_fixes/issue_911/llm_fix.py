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

    # FIX: qargs[1] assumes two operands and Qubit has no public register/index -> inspect every operand with find_bit, because gates may be single-qubit and find_bit is the supported lookup
    for qarg in qargs:
        bit_location = qc.find_bit(qarg)
        print("qarg : ", qarg)
        print("register : ", bit_location.registers)
        print("index : ", bit_location.index)
