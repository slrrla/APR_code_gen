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

# FIX: unpacking order [control, train_register] swapped the registers -> unpack as [train_register, control], because circ.qregs follows the constructor order (train_register first)
[train_register, control] = circ.qregs
circ.h(control)

oracle = create_oracle(train_register, control)
# FIX: passing a list of two registers gave 2 qargs instead of 4 qubits -> flatten registers into one qubit list, because append expects one qarg per instruction qubit
circ.append(oracle, [*train_register, *control])
