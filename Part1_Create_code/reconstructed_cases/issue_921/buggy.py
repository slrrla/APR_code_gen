from qiskit.aqua import run_algorithm
from qiskit.aqua.input import EnergyInput
from qiskit.aqua.operators import WeightedPauliOperator

# Minimal qubit operator standing in for the Max-Cut Ising Hamiltonian
pauli_dict = {
    'paulis': [{"coeff": {"imag": 0.0, "real": 1.0}, "label": "ZZII"}]
}
qubitOp = WeightedPauliOperator.from_dict(pauli_dict)
algo_input = EnergyInput(qubitOp)

algorithm_cfg = {
    'name': 'ExactEigensolver',
}
params = {
    'problem': {'name': 'ising'},
    'algorithm': algorithm_cfg
}
result = run_algorithm(params, algo_input)
print(result)
