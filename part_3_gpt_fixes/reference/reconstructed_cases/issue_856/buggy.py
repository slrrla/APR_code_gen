from qiskit.opflow.evolutions.trotterizations.qdrift import QDrift
from qiskit.opflow import X, Y

sim = QDrift(1)
pauli = (X ^ X) + (Y ^ Y)

com_op = sim.convert(pauli)

# This raises: qiskit.extensions.exceptions.ExtensionError: 'Input matrix is not unitary.'
circ = com_op.to_circuit()
