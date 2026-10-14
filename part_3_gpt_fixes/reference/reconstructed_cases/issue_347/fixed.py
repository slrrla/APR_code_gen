import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit.opflow import StateFn, CircuitStateFn, PauliExpectation, CircuitSampler, Z
from qiskit.opflow.list_ops import ListOp
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

# batch all measurable expressions into a single ListOp so only one job is submitted
measurable_expressions_list = []
for i, inp in enumerate(x):
    parameters = {list(a.parameters)[0]: inp}
    ψ = CircuitStateFn(a.assign_parameters(parameters))
    measurable_expression = StateFn(h, is_measurement=True).compose(ψ)
    measurable_expressions_list.append(measurable_expression)

expect_ops = PauliExpectation().convert(ListOp(measurable_expressions_list))
sampler = CircuitSampler(quantum_instance)
sampled_ops = sampler.convert(expect_ops)
expectation_values = sampled_ops.eval()

for i, exp_val in enumerate(expectation_values):
    y[i] = exp_val.real
    z[i] = exp_val.imag

print(y, z)
