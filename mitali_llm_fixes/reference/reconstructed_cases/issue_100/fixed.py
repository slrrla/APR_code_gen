from qiskit.circuit import QuantumCircuit
from qiskit import Aer, transpile
from qiskit.compiler import assemble

c = QuantumCircuit(2)
c.measure_all()
simulator = Aer.get_backend('qasm_simulator')
c = transpile(c, simulator)
my_qobj = assemble(c)
result = simulator.run(my_qobj).result()
counts = result.get_counts()
print(counts)
