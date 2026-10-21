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

# FIX: unpacking order was swapped relative to circ.qregs -> unpack as [train_register, control], because the circuit was built with train_register first
[train_register, control] = circ.qregs
circ.h(control)

oracle = create_oracle(train_register, control)
# FIX: passing a list of registers gave 2 qargs instead of 4 -> flatten registers into individual qubits, because append expects one entry per qubit and this works for any register length
circ.append(oracle, [*train_register, *control])
