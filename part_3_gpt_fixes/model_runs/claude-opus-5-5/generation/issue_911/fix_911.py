import qiskit
from qiskit.circuit.random import random_circuit

num_qubits = 3
depth = 1
max_operands = 2
qc = random_circuit(num_qubits, depth, max_operands=max_operands, seed=1)
qc = qc.decompose(reps=3)

# FIX: tuple-unpacking CircuitInstruction is deprecated/removed -> read operation/qubits/clbits attributes, because that is the supported API
for instruction in qc.data:
    name_of_gate, qargs, cargs = instruction.operation, instruction.qubits, instruction.clbits
    print("name of gate : ", name_of_gate)
    print("qargs : ", qargs, "\n")

    # FIX: single-qubit gates have no qargs[1] -> guard on len(qargs) > 1, because indexing would raise IndexError
    if len(qargs) > 1:
        print("qargs[1] : ", qargs[1])
        # FIX: Qubit is not subscriptable and has no .register/.index -> use qc.find_bit(), because it returns the circuit index and (register, index) pairs
        print("qargs[1][1] : ", qc.find_bit(qargs[1]).index)
        print("qargs[1].register : ", qc.find_bit(qargs[1]).registers[0][0])
        print("qargs[1].index : ", qc.find_bit(qargs[1]).registers[0][1])
