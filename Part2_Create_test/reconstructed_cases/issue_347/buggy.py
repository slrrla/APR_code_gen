import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit.opflow import StateFn, CircuitStateFn, PauliExpectation, CircuitSampler, Z
from qiskit.utils import QuantumInstance
from qiskit.providers.aer import AerSimulator

# simple parametrized ansatz
theta = Parameter('theta')
a = QuantumCircuit(1)
a.h(0)
a.rz(theta, 0)

# operator whose expectation value we want
h = Z

quantum_instance = QuantumInstance(AerSimulator())

x = np.linspace(0, 2 * np.pi, 10)
y = np.zeros(len(x))
z = np.zeros(len(x))

# submits one job per input value -- slow, each iteration queues separately
for i, inp in enumerate(x):
    parameters = {list(a.parameters)[0]: inp}
    ψ = CircuitStateFn(a.assign_parameters(parameters))
    measurable_expression = StateFn(h, is_measurement=True).compose(ψ)
    expectation = PauliExpectation().convert(measurable_expression)
    sampler = CircuitSampler(quantum_instance).convert(expectation)
    y[i] = sampler.eval().real
    z[i] = sampler.eval().imag

print(y, z)
