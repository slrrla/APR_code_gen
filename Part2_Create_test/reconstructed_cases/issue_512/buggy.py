from qiskit import QuantumCircuit, Aer
from qiskit.aqua import QuantumInstance
# NOTE: qiskit.aqua.operators is the deprecated Aqua operator module
from qiskit.aqua.operators import (
    X, Y, Z, I,
    StateFn,
    CircuitStateFn,
    CircuitOp,
    PauliExpectation,
    AerPauliExpectation,
    MatrixExpectation,
    CircuitSampler,
    WeightedPauliOperator,
)

# you can define your operator as circuit
circuit = QuantumCircuit(2)
circuit.z(0)
circuit.z(1)
op = CircuitOp(circuit)  # and convert to an operator

# or if you have a WeightedPauliOperator, do
# op = weighted_pauli_op.to_opflow()

# but here we'll use the H2-molecule Hamiltonian
op = (-1.0523732 * I ^ I) + (0.39793742 * I ^ Z) + (-0.3979374 * Z ^ I) \
    + (-0.0112801 * Z ^ Z) + (0.18093119 * X ^ X)

# define the state you w.r.t. which you want the expectation value
psi = QuantumCircuit(2)
psi.x(0)
psi.x(1)
# convert to a state
psi = CircuitStateFn(psi)

# easy expectation value, use for small systems only!
print('Math:', psi.adjoint().compose(op).compose(psi).eval().real)

# define your backend or quantum instance (where you can add settings)
backend = Aer.get_backend('qasm_simulator')
q_instance = QuantumInstance(backend, shots=1024)

# define the state to sample
measurable_expression = StateFn(op, is_measurement=True).compose(psi)

# convert to expectation value
expectation = PauliExpectation().convert(measurable_expression)

# get state sampler (you can also pass the backend directly)
sampler = CircuitSampler(q_instance).convert(expectation)

# evaluate
print('Sampled:', sampler.eval().real)

expectation = AerPauliExpectation().convert(measurable_expression)
sampler = CircuitSampler(backend).convert(expectation)
print('Snapshot:', sampler.eval().real)

expectation = MatrixExpectation().convert(measurable_expression)
sampler = CircuitSampler(backend).convert(expectation)
print('Matrix:', sampler.eval().real)
