from qiskit.quantum_info import Statevector

n = Statevector([(1+2.0j)/3, -2/3])
n.measure
