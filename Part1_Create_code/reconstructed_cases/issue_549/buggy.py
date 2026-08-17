from qiskit.quantum_info import SparsePauliOp

# ZX means Z on the first qubit and X on the second qubit
operator = SparsePauliOp.from_list([("ZX", 1.0)])  # Not sure what is the second parameter?
print(operator)

from qiskit import QuantumCircuit
qc = QuantumCircuit(2)
qc.z(0)
qc.x(1)
print(qc.draw())
