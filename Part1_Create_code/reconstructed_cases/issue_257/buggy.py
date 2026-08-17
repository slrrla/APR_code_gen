import numpy as np
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import UCRYGate
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime.fake_provider import FakeKolkata
from qiskit_aer import Aer
from qiskit_aer.noise import NoiseModel
from qiskit_aer import AerSimulator
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
qc1.measure_all()

shots_used = 10000
print("Circuit depth: ", qc2.depth())
print("Circuit gate counts:", qc2.count_ops())

# Bug: AerSimulator exposes a huge native basis gate set, so transpiling
# against it does not actually decompose the circuit down to hardware-level
# basis gates as the user expected.
backend = AerSimulator()
pm = generate_preset_pass_manager(backend=backend, optimization_level=3)
qc_optimized = pm.run(qc1)

print("Optimzied circuit depth: ", qc_optimized.depth())
print("Optimized gate counts:", qc_optimized.count_ops())
print(qc_optimized.draw())

job = backend.run(qc_optimized, shots=shots_used)
result = job.result()
counts = result.get_counts(qc_optimized)
