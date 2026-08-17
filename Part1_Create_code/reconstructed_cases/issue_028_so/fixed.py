from qiskit import QuantumCircuit, execute
from qiskit import Aer
from qiskit.providers.aer.noise import NoiseModel, depolarizing_error

ckt = QuantumCircuit(2, 2)
ckt.h(0)
ckt.cx(0, 1)
ckt.measure(0, 0)
ckt.measure(1, 1)

qsim = Aer.get_backend("qasm_simulator")

# Build a simple local noise model (no hardware/IBMQ access needed)
noise_model = NoiseModel()
error = depolarizing_error(0.01, 1)
noise_model.add_all_qubit_quantum_error(error, ['u1', 'u2', 'u3'])

job = execute(
    ckt,
    qsim,
    noise_model=noise_model,
    basis_gates=noise_model.basis_gates
)

result = job.result()
print(result.get_counts())
