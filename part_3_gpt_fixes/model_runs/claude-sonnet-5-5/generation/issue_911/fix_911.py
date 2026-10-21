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

    # FIX: single-qubit gates have no qargs[1] and Qubit has no subscript/register/index -> use the last qubit and qc.find_bit(), because find_bit returns the index and register of a bit
    loc = qc.find_bit(qargs[-1])
    print("qargs[-1] : ", qargs[-1])
    print("qargs[1][1] : ", loc.registers[0][1])
    print("qargs[1].register : ", loc.registers[0][0])
    print("qargs[1].index : ", loc.index)
