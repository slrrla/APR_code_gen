from qiskit import QuantumCircuit

qc = QuantumCircuit(2)
# second argument to x() is a "label", which should be a string or None.
# Passing an int (1) here triggers a TypeError deep inside the mpl drawer
# when qc.draw() is called (defaults to 'mpl' if matplotlib is installed).
qc.x(0, 1)
qc.draw()
