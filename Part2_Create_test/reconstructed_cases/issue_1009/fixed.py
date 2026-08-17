import numpy as np
from qiskit import QuantumCircuit
from qiskit.utils import QuantumInstance
from qiskit.providers.aer import AerSimulator
from qiskit.opflow import X, Z, I, StateFn, ListOp, CircuitSampler
from qiskit.opflow.expectations import ExpectationFactory

# simple circuit to evaluate expectation values on
circuit = QuantumCircuit(2)
circuit.h(0)
circuit.cx(0, 1)

# use Aer qasm simulator with a fixed number of shots
backend = AerSimulator()
quantum_instance = QuantumInstance(backend, shots=10)

observables = [
    X ^ X,
    Z ^ I,
    Z ^ Z,
]

circuit_sampler = CircuitSampler(quantum_instance)

# setting include_custom=False forces PauliExpectation to be used
# instead of AerPauliExpectation, so the requested number of shots
# is respected instead of being ignored.
exp_converter = ExpectationFactory.build(observables[0], quantum_instance, include_custom=False)  # <== here

list_op = ListOp([StateFn(obs, is_measurement=True).compose(StateFn(circuit)) for obs in observables])

observables_expect = exp_converter.convert(list_op)
observables_expect_sampled = circuit_sampler.convert(observables_expect)
observables_results = np.real(observables_expect_sampled.eval())
print(observables_results)
