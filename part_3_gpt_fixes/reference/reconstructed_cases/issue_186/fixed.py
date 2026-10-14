# Fixed: add 'save_density_matrix' to the set of gates ParamShift considers
# supported, so the internal transpile step does not fail while trying to
# translate the circuit's basis into the gradient's target basis.

from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
import qiskit.providers.aer  # registers save_density_matrix() on QuantumCircuit
from qiskit.opflow import CircuitStateFn, Gradient, Z
from qiskit.opflow.gradients.circuit_gradients.param_shift import ParamShift

# Patch the supported gate set used by the parameter-shift gradient method
# to include the save_density_matrix instruction present in our circuit.
ParamShift.SUPPORTED_GATES = ParamShift.SUPPORTED_GATES | {'save_density_matrix'}

theta = Parameter('theta')
qc = QuantumCircuit(2)
qc.h(0)
qc.ry(theta, 0)
qc.cx(0, 1)
qc.save_density_matrix()

op = Z ^ Z
state = CircuitStateFn(qc)
expectation = op @ state

shifter = Gradient()  # parameter-shift rule is the default
grad = shifter.convert(expectation, params=theta)

value_dict = {theta: 0.5}
result = grad.assign_parameters(value_dict).eval()
print(result)
