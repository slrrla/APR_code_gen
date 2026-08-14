from qiskit import QuantumCircuit

circ = QuantumCircuit(2)
circ.draw()

a = ('cx', 0, 1)
getattr(circ, a[0])(a[1], a[2])
circ.draw()
