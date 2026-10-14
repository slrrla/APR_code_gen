from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

# Build a 2-qubit circuit
qc = QuantumCircuit(2)

# This calculates what the state vector of our qubits would be
# after passing through the circuit 'qc'
ket = Statevector(qc)

# The code below writes down the state vector.
# Since it's the last line in the cell, the cell will display it as output
ket.draw()

# Now apply X gate on qubit 0
qc.x(0)
ket = Statevector(qc)
ket.draw()
