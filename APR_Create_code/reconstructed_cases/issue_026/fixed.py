from qiskit import QuantumCircuit

qc = QuantumCircuit(2)
# pass a proper string label as the second argument instead of an int
qc.x(0, '1')
qc.draw('mpl')
