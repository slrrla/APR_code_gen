import numpy as np
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit import Parameter
from qiskit.opflow import StateFn, CircuitStateFn, Gradient, X, Z

# Instantiate the quantum state
a = Parameter('a')
b = Parameter('b')
q = QuantumRegister(1)
qc = QuantumCircuit(q)
qc.h(q)
qc.rz(a, q[0])
qc.rx(b, q[0])
params = [a, b]

# Instantiate the Hamiltonian observable
H = 0.5 * X - 1 * Z

# Combine the Hamiltonian observable and the state
op = ~StateFn(H) @ CircuitStateFn(primitive=qc, coeff=1.)

value_dict = {a: np.pi / 4, b: np.pi}

state_grad = Gradient(grad_method='param_shift').convert(operator=op, params=params)
state_grad_assigned = state_grad.assign_parameters(value_dict)

# Bug: evaluates exactly, ignoring any noisy/simulator backend
result = state_grad_assigned.eval()
print(result)
