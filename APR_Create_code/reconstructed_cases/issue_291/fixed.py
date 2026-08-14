import numpy as np
from qiskit import QuantumCircuit

circuit = QuantumCircuit(2)
initial_state0 = [1/np.sqrt(2), 1/np.sqrt(2)]
circuit.initialize(initial_state0, 0)
initial_state1 = [1, 0]
circuit.initialize(initial_state1, 1)
circuit.cx(0, 1)

from qiskit_experiments.library import StateTomography
from qiskit.providers.aer import Aer

backend = Aer.get_backend('qasm_simulator')

# QST Experiment on qubit 1 only
qstexp1 = StateTomography(circuit, measurement_qubits=[1])
qstdata1 = qstexp1.run(backend, seed_simulation=1000).block_for_results()

# Print results
for result in qstdata1.analysis_results():
    print(result)
