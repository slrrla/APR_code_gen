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

# FIX: Register unpacking reversed their roles -> match the circuit's register order, because control must refer to the control register.
[train_register, control] = circ.qregs
circ.h(control)

oracle = create_oracle(train_register, control)
# FIX: Nested registers did not supply individual qubit arguments -> flatten them in oracle order, because append requires one argument per instruction qubit.
circ.append(oracle, list(train_register) + list(control))
