import numpy as np
from qiskit.circuit.library import TwoLocal
from qiskit.primitives import Estimator
from qiskit.quantum_info import SparsePauliOp
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import Estimator as AerEstimator
from qiskit_ibm_runtime import EstimatorV2

seed = 20
n_qubits = 2

obs = SparsePauliOp(
    ['ZY', 'YI', 'IY', 'II', 'YY', 'ZY', 'XI', 'YZ', 'ZZ', 'IX'],
    coeffs=[0.64414354+0.j, 0.38074849+0.j, 0.66304791+0.j, 0.16365073+0.j,
            0.96260781+0.j, 0.34666184+0.j, 0.99175099+0.j, 0.2350579+0.j,
            0.58569427+0.j, 0.4066901+0.j]
)

# Ansatz
circuit = TwoLocal(
    n_qubits,
    ["rx", "ry", "rz"],
    ["cx"],
    "linear",
    reps=3,
)

params = np.random.uniform(low=0, high=2 * np.pi, size=circuit.num_parameters)

# Estimator V2
aer_sim = AerSimulator(method="automatic")
pm = generate_preset_pass_manager(backend=aer_sim, optimization_level=1)
isa_qc = pm.run(circuit)

est = EstimatorV2(backend=aer_sim, options={"seed_estimator": seed})  # set the seed_estimator option
pub = (isa_qc, obs, params)
result = est.run([pub]).result()
print(f"Expectation value from Estimatorv2: {result[0].data.evs}")

# Aer Estimator
est = AerEstimator(run_options={"seed": seed}, approximation=True)  # changed to approximation=True
result = est.run([isa_qc], [obs], [params]).result()
print(f"Expectation value from AerEstimator: {result.values[0]}")

# Primitive Estimator
est = Estimator(options={"seed": seed})
result = est.run([isa_qc], [obs], [params]).result()
print(f"Expectation value from qiskit.primitve Estimator: {result.values[0]}")
