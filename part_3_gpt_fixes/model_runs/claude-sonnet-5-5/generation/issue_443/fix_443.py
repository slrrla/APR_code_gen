from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit import Gate

def create_oracle(train_register, control):
    n = len(train_register) + len(control)
    qc = QuantumCircuit(n, name="oracle")
    qc.x(n - 1)
    return qc.to_instruction()

train_register = QuantumRegister(3, name="train_register")
control = QuantumRegister(1, name="control")

circ = QuantumCircuit(train_register, control)

# FIX: registers unpacked in the wrong order -> swapped to match the order they were added to the circuit, because circ.qregs is [train_register, control]
[train_register, control] = circ.qregs
circ.h(control)

oracle = create_oracle(train_register, control)
# FIX: passed a list of two registers (2 qargs) -> flatten the registers into a list of individual qubits, because the 4-qubit instruction needs 4 qubit arguments
circ.append(oracle, [*train_register, *control])
