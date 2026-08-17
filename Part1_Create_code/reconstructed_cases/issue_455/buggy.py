from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit.quantum_info import Statevector

q = QuantumRegister(1)
c = ClassicalRegister(1)
qc = QuantumCircuit(q, c)

qc.draw('mpl')

# In this (older) version of qiskit, Statevector() cannot be constructed
# directly from a QuantumCircuit -- it expects a numpy array, list,
# Statevector, or Operator.  Passing the circuit directly raises:
# QiskitError: 'Invalid input data format for Statevector'
psi1 = Statevector(qc)
psi1.draw('latex')
