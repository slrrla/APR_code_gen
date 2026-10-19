import numpy as np
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit import Parameter
from qiskit.opflow import StateFn, CircuitStateFn, Gradient, X, Z, CircuitSampler, AerPauliExpectation
from qiskit_aer.backends import AerSimulator

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

# Use CircuitSampler to evaluate on a simulator/backend
simulator = AerSimulator()
sampler = CircuitSampler(simulator)

# for efficiency: don't manually bind the parameters, but let the sampler do it!
sampled = sampler.convert(state_grad, value_dict)

# now call eval to evaluate the sampled circuits
result = sampled.eval()
print(result)
