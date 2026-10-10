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

[control, train_register] = circ.qregs
circ.h(control)

oracle = create_oracle(train_register, control)
# FIX: Two registers were passed as qargs -> flatten them into an ordered qubit list, because the instruction requires one argument per qubit.
circ.append(oracle, list(train_register) + list(control))

