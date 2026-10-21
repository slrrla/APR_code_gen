from qiskit.aqua import run_algorithm
from qiskit.aqua.input import EnergyInput
from qiskit.aqua.operators import WeightedPauliOperator

pauli_dict = {
    'paulis': [{"coeff": {"imag": 0.0, "real": 1.0}, "label": "ZZII"}]
}
qubitOp = WeightedPauliOperator.from_dict(pauli_dict)
algo_input = EnergyInput(qubitOp)

algorithm_cfg = {
    'name': 'ExactEigensolver',
}
params = {
    # FIX: problem name 'ising' did not match the EnergyInput operator input -> changed it to 'energy', because EnergyInput is the input for the 'energy' problem and this needs no Ising-specific handling
    'problem': {'name': 'energy'},
    'algorithm': algorithm_cfg
}
result = run_algorithm(params, algo_input)
print(result)
