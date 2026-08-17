from qiskit.aqua.algorithms import ExactEigensolver
from qiskit.aqua.operators import WeightedPauliOperator

# Minimal qubit operator standing in for the Max-Cut Ising Hamiltonian
pauli_dict = {
    'paulis': [{"coeff": {"imag": 0.0, "real": 1.0}, "label": "ZZII"}]
}
qubitOp = WeightedPauliOperator.from_dict(pauli_dict)

ee = ExactEigensolver(qubitOp, k=1)
result = ee.run()
print(result)
