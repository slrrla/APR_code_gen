import numpy as np
import pdb
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import UCRYGate
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler  # Not sure what is the need for this
from qiskit_aer import Aer
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime.fake_provider import FakeKolkataV2
from qiskit_ibm_runtime.fake_provider import FakeBrisbane, FakeSherbrooke
from qiskit_aer.noise import NoiseModel
import math

backend = FakeKolkataV2()
noise_model = NoiseModel.from_backend(backend)
coupling_map = backend.coupling_map

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

qc = qc1.compose(qc2, list(range(0, num_qubits)))
qc.measure_all()

# FIX: use AerSimulator directly with noise_model/coupling_map so the noise
# actually gets injected into the simulation.
simulator = AerSimulator(noise_model=noise_model, coupling_map=coupling_map)

pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
circuit_opt = pm.run(qc)
print(circuit_opt.draw())

job = simulator.run(circuit_opt, noise_model=noise_model, shots=1000)
result = job.result()
counts = result.get_counts(circuit_opt)
print(counts)
