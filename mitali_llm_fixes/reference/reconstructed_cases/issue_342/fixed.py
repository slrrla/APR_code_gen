import math
from qiskit import QuantumCircuit, transpile
from qiskit.providers.aer import AerSimulator

circ = QuantumCircuit(5)
circ.h(range(5))
circ.save_density_matrix(qubits=[0, 1])  # <== here
circ.measure_all()

simulator = AerSimulator()
circ = transpile(circ, backend=simulator)
job = simulator.run(circ)
state = job.result().data()['density_matrix']

state.draw('latex')

# Check state purity:
if math.isclose(state.purity().real, 1):
    # Get the state vector
    sv = state.to_statevector()

sv.draw('latex')
