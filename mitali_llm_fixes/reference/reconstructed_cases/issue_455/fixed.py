from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit.quantum_info import Statevector

q = QuantumRegister(1)
c = ClassicalRegister(1)
qc = QuantumCircuit(q, c)

qc.draw('mpl')

# Use Statevector.from_instruction() to build the statevector from a
# QuantumCircuit instead of passing the circuit directly to the constructor.
psi1 = Statevector.from_instruction(qc)
psi1.draw('latex')
