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

# FIX: unpacking order [control, train_register] did not match circ.qregs order (train_register, control), swapping the names -> changed to [train_register, control] to match the creation order, because H must act on the 1-qubit control register
[train_register, control] = circ.qregs
circ.h(control)

oracle = create_oracle(train_register, control)
# FIX: passed a list of QuantumRegisters as qargs, which append() does not accept (it needs individual qubits) -> flattened the registers into a list of qubits, because the oracle's qubit count is the total number of register qubits
circ.append(oracle, list(train_register) + list(control))
