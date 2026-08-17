from qiskit import QuantumCircuit, execute, Aer
from qiskit.quantum_info import Statevector

# Build the circuit once (no measurement, so the statevector survives)
qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)

def get_statevector(qc, show=True) -> Statevector:
    sim = Aer.get_backend('aer_simulator')
    qc = qc.copy()
    qc.save_statevector()
    result = execute(qc, sim).result()
    vector = result.get_statevector()
    if show:
        display(Statevector(vector).draw('latex'))
    return vector

# Perform the linear algebra only once...
vector = get_statevector(qc, show=False)

# ...then draw many samples from the resulting statevector directly,
# avoiding re-simulation of the circuit for every shot.
counts = Statevector(vector).sample_counts(shots=1000000)
print(counts)
