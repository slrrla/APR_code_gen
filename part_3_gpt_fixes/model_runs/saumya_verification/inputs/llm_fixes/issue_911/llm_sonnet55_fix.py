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

    # FIX: used removed Qubit attributes (register/index/subscripting) and qargs[1] on 1-qubit gates -> loop over qargs and use qc.find_bit(qubit), because Qubit no longer stores its register or index and find_bit returns them (and the loop avoids an IndexError for single-qubit gates)
    for qubit in qargs:
        print("qubit : ", qubit)
        print("register, index : ", qc.find_bit(qubit).registers)
        print("index : ", qc.find_bit(qubit).index)
