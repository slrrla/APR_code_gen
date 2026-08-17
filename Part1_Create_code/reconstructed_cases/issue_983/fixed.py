from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator, SparsePauliOp
from qiskit_aer import AerSimulator

# Operator circuit representing the non-local operator O
operator_circ = QuantumCircuit(4)
operator_circ.x(0)
operator_circ.cz([1, 1, 2], [2, 3, 3])

# Explicitly decompose the operator into weighted (sparse) Paulis
operator = SparsePauliOp.from_operator(Operator(operator_circ))

# Some state |psi> for which we want <psi|O|psi>
psi = QuantumCircuit(4)
psi.h(0)
psi.cx(0, 1)
psi.cx(1, 2)
psi.cx(2, 3)

# Using the SparsePauliOp form for the expectation value
psi.save_expectation_value(operator, range(4))

backend = AerSimulator()
result = backend.run(psi).result()
print(result.data(0)['expectation_value'])
