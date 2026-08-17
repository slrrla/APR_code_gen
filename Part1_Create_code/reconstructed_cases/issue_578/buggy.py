from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator
from qiskit.primitives import Estimator

# Observable
X = Operator([[0, 1], [1, 0]])
M_hat = X.tensor(X).tensor(X).tensor(X).tensor(X).tensor(X)

# Quantum circuit with mid-circuit measurements and resets
psi = QuantumCircuit(6, 2)
psi.x(0)
psi.h(1)
psi.measure(0, 0)
psi.measure(1, 1)
psi.reset(0)
psi.reset(1)

# This fails because the circuit still contains classical measure instructions
estimator = Estimator(options={"shots": 1})
expectation_value = estimator.run(psi, M_hat, run_options={"shots": 1}).result().values
print("expectation: ", expectation_value)
