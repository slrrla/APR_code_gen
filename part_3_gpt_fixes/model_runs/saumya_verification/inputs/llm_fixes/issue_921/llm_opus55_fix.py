# FIX: qiskit.aqua (run_algorithm, EnergyInput, WeightedPauliOperator) was removed from Qiskit -> import numpy and SparsePauliOp instead, because the aqua imports no longer exist and crash
import numpy as np
from qiskit.quantum_info import SparsePauliOp

pauli_dict = {
    'paulis': [{"coeff": {"imag": 0.0, "real": 1.0}, "label": "ZZII"}]
}
# FIX: WeightedPauliOperator.from_dict no longer exists -> build a SparsePauliOp from the same dict, because SparsePauliOp is the current Pauli operator class
qubitOp = SparsePauliOp.from_list([(p['label'], complex(p['coeff']['real'], p['coeff']['imag'])) for p in pauli_dict['paulis']])
# FIX: EnergyInput wrapper was removed -> use the operator directly, because the modern API takes the operator itself
algo_input = qubitOp

algorithm_cfg = {
    'name': 'ExactEigensolver',
}
params = {
    'problem': {'name': 'ising'},
    'algorithm': algorithm_cfg
}
# FIX: run_algorithm was removed -> compute the exact minimum eigenvalue with numpy, because this is what ExactEigensolver did for the ising problem
result = {'energy': float(np.min(np.linalg.eigvalsh(algo_input.to_matrix())))}
print(result)
