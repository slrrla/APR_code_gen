from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

# Build a 2-qubit circuit and apply an X gate on qubit 0
qc = QuantumCircuit(2)
qc.x(0)

# This calculates what the state vector of our qubits would be
# after passing through the circuit 'qc'
ket = Statevector(qc)

# Qiskit uses the "little endian" bit ordering convention: qubit 0 is the
# least-significant bit. So applying X on qubit 0 turns |00> into |01>,
# i.e. the second basis state, which is why the amplitude at index 1 is 1.
print(ket)

# dims() does NOT give the size of the statevector; it gives the dimension
# of each individual subsystem (here: two qubits, each of dimension 2),
# hence dims=(2, 2) rather than (4, 1).
print(ket.dims())
