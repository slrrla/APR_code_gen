from qiskit import QuantumCircuit

qc = QuantumCircuit(1, 1)
qc.x(0)
qc.y(0)
qc.rz(1, 0)
print(qc)
# Bug: forgot to call depth() as a method -- this just prints the bound
# method object instead of the actual circuit depth value.
print("The circuit depth is:", qc.depth)
