import numpy as np
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import UCRYGate
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime.fake_provider import FakeKolkata
from qiskit_ibm_runtime.fake_provider import FakeBrisbane, FakeSherbrooke
from qiskit_aer import Aer
from qiskit_aer.noise import NoiseModel
import math
import pdb

num_qubits = 3
data = np.array([
    [0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0]
])
angles = [np.pi / 4, np.pi / 2, 3 * np.pi / 4, np.pi]
controls = [0, 1]
target = [2]

qr1 = QuantumRegister(num_qubits, name='q')
qc1 = QuantumCircuit(qr1)
qc1.append(UCRYGate(angles), controls + target)
qc1.append(UCRYGate(angles), controls + target)

qr2 = QuantumRegister(num_qubits, name='q')
qc2 = QuantumCircuit(qr2)
qc2.unitary(data, qr2, label='u')

qc1 = qc1.compose(qc2, list(range(0, num_qubits)))
qc1 = qc1.decompose()  # Decomposing the quantum circuit
print(qc1.draw())
qc1.measure_all()
# print(qc1.draw())

shots_used = 10000
print("Circuit depth: ", qc2.depth())
print("Circuit gate counts:", qc2.count_ops())

# backend_fake = FakeKolkata()
backend_fake = FakeSherbrooke()
noise_model = NoiseModel.from_backend(backend_fake)
print(noise_model)
coupling_map = backend_fake.coupling_map

# BUG: passing noise_model/coupling_map directly to Aer.get_backend() has no effect;
# qasm_simulator backend does not accept these kwargs this way.
backend = Aer.get_backend('qasm_simulator', noise_model=noise_model, coupling_map=coupling_map)

pm = generate_preset_pass_manager(backend=backend, optimization_level=3)
qc_optimized = pm.run(qc1)
# pdb.set_trace()
print("Optimzied circuit depth: ", qc_optimized.depth())
print("Optimized gate counts:", qc_optimized.count_ops())
# pdb.set_trace()
print(qc_optimized.draw())

job = backend.run(qc_optimized, noise_model=noise_model, shots=shots_used)
result = job.result()
counts = result.get_counts(qc_optimized)
print(counts)
