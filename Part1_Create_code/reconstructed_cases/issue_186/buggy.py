# Minimal reproduction of "Unable to map source basis ... save_density_matrix" error
# when computing a gradient with qiskit's opflow Gradient/ParamShift.

from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
import qiskit.providers.aer  # registers save_density_matrix() on QuantumCircuit
from qiskit.opflow import CircuitStateFn, Gradient, Z

# Build a parametrized circuit that includes a save_density_matrix instruction,
# similar to the more complex circuit used in the reported case.
theta = Parameter('theta')
qc = QuantumCircuit(2)
qc.h(0)
qc.ry(theta, 0)
qc.cx(0, 1)
qc.save_density_matrix()  # this instruction is not in ParamShift.SUPPORTED_GATES

# Build an expectation value expression over the circuit's state.
op = Z ^ Z
state = CircuitStateFn(qc)
expectation = op @ state

# Attempt to compute the gradient of the expectation value w.r.t. theta.
shifter = Gradient()  # parameter-shift rule is the default
grad = shifter.convert(expectation, params=theta)

value_dict = {theta: 0.5}
result = grad.assign_parameters(value_dict).eval()
print(result)
