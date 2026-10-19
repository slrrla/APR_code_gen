# NO BUG: This is valid Aqua usage; the Ising problem entry selects the problem interface while ExactEigensolver operates on the supplied EnergyInput.
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
    'problem': {'name': 'ising'},
    'algorithm': algorithm_cfg
}
result = run_algorithm(params, algo_input)
print(result)
