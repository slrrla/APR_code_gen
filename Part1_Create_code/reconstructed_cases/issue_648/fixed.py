import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter, ParameterVector

def outer_circuit(subcircuit, imaginary=False):
    qc = QuantumCircuit(4, 1)
    qc.append(subcircuit, qc.qubits)
    # operations
    return qc

def subcircuit():
    global a
    a = ParameterVector('a', 9)
    m, n = Parameter('m'), Parameter('n')
    qc = QuantumCircuit(4, name='V')
    # random operations which use parameters
    qc.rx(a[0], 0)
    qc.ry(m, 1)
    qc.rz(n, 2)
    return qc.to_instruction()

operator = subcircuit()
print(operator.parameters)
test = outer_circuit(operator)
print(test.parameters)

test.bind_parameters({a: np.random.rand(9)})
