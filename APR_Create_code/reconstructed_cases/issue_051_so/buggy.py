from qiskit import *
from qiskit.circuit.library import *
from qiskit.providers.aer import *

sim = AerSimulator(method='statevector')
shots = 100
depth = 10
qubits = 5  # reduced from 35 for practicality
circuit = transpile(QuantumVolume(qubits, depth, seed=0),
                     backend=sim,
                     optimization_level=0)
circuit.measure_all()
result = execute(circuit, sim, shots=shots, seed_simulator=12345).result()
if result.to_dict()['metadata']['mpi_rank'] == 0:
    print(result.to_dict()['metadata'])
