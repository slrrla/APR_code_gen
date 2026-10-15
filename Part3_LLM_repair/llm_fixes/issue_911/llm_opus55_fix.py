import qiskit
from qiskit.circuit.random import random_circuit

num_qubits = 3
depth = 1
max_operands = 2
qc = random_circuit(num_qubits, depth, max_operands=max_operands, seed=1)
qc = qc.decompose(reps=3)

# FIX: tuple-unpacking CircuitInstruction may not be supported in newer Qiskit -> read operation/qubits/clbits attributes, because they are the stable API
for instruction in qc.data:
    name_of_gate, qargs, cargs = instruction.operation, instruction.qubits, instruction.clbits
    print("name of gate : ", name_of_gate)
    print("qargs : ", qargs, "\n")

    # FIX: Qubit has no index/register attributes, is not subscriptable, and single-qubit gates have no qargs[1] -> guard length and use qc.find_bit, because find_bit returns the circuit index and (register, index) pairs
    if len(qargs) > 1:
        print("qargs[1] : ", qargs[1])
        print("qargs[1][1] : ", qc.find_bit(qargs[1]).registers[0][1])
        print("qargs[1].register : ", qc.find_bit(qargs[1]).registers[0][0])
        print("qargs[1].index : ", qc.find_bit(qargs[1]).index)
