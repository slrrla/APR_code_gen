from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit import Gate

def create_oracle(train_register, control):
    # returns an Instruction acting on all qubits of train_register + control
    n = len(train_register) + len(control)
    qc = QuantumCircuit(n, name="oracle")
    qc.x(n - 1)
    return qc.to_instruction()

train_register = QuantumRegister(3, name="train_register")
control = QuantumRegister(1, name="control")

circ = QuantumCircuit(train_register, control)

# initialising registers for readability
[train_register, control] = circ.qregs
circ.h(control)

# create and append oracle
oracle = create_oracle(train_register, control)  # returns an Instruction
circ.append(oracle, list(train_register) + list(control))
