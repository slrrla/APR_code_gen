import time

from qiskit.circuit.library import TwoLocal
from qiskit.quantum_info import SparsePauliOp
from qiskit.algorithms.optimizers import NFT
from qiskit.algorithms.minimum_eigensolvers import VQE
from qiskit_ibm_runtime import QiskitRuntimeService, Options, Estimator

service = QiskitRuntimeService(token="YOUR-TOKEN", channel="ibm_quantum")
options = Options()
options.optimization_level = 3
options.execution.shots = 100
backend = service.backend("ibmq_qasm_simulator")
estimator = Estimator(session=backend, options=options)

hamiltonian_0 = SparsePauliOp(["IIII"])
hamiltonian_1 = SparsePauliOp(
    [
        "IIII", "IIIZ", "IIZI", "IIZZ", "IZII", "IZIZ", "IZZI", "IZZZ",
        "ZIII", "ZIIZ", "ZIZI", "ZIZZ", "ZZII", "ZZIZ", "ZZZI", "ZZZZ",
    ],
    coeffs=[1.0] * 16,
)

dim = hamiltonian_0.num_qubits
ansatz = TwoLocal(
    dim,
    rotation_blocks=["ry"],
    entanglement="reverse_linear",
    entanglement_blocks="cx",
    reps=1,
)
optimizer = NFT(maxiter=100)
vqe = VQE(estimator=estimator, ansatz=ansatz, optimizer=optimizer)

for name, hamiltonian in (("hamiltonian_0", hamiltonian_0), ("hamiltonian_1", hamiltonian_1)):
    start = time.time()
    result = vqe.compute_minimum_eigenvalue(hamiltonian)
    print(name, result.optimizer_time, time.time() - start)
