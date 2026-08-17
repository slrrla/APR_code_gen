from qiskit.circuit import QuantumCircuit
from qiskit import Aer, transpile

c = QuantumCircuit(2)
c.measure_all()
simulator = Aer.get_backend('qasm_simulator')
c = transpile(c, simulator)
result = simulator.run(c).result()
counts = result.get_counts()
print(counts)
