from qiskit import transpile
from qiskit.circuit.library import QuantumVolume

# Build a circuit and transpile it to u3/cx basis
qc = QuantumVolume(2)
tqc = transpile(qc, optimization_level=3, basis_gates=["u3", "cx"], seed_transpiler=1)

# The only way to inspect the U3 gate parameters is to draw the circuit
# and read them off one by one -- there is no programmatic extraction.
tqc.draw()
