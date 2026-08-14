from qiskit import QuantumCircuit, execute
from qiskit import Aer
from numpy import pi, array, sqrt
from numpy.linalg import norm

data = array([-0.5, -0.2, -0.2, -0.6])
norm_data = norm(data)
normalized_data = data / norm_data

qasm_sim = Aer.get_backend('qasm_simulator')
statevector_sim = Aer.get_backend('statevector_simulator')

def create_qc():
    qc = QuantumCircuit(2)
    qc.initialize(normalized_data, [0, 1])
    qc.h(0)
    qc.cx(0, 1)
    qc.x(0)
    qc.rx(-pi/10, 0)
    qc.ry(-pi/20, 1)
    return qc

# qasm simulator
qc = create_qc()
qc.measure_all()
result = execute(qc, qasm_sim, shots=10000).result()
counts = result.get_counts()
print('qasm simulator:', [
    sqrt(counts['00'] / 10000),
    sqrt(counts['01'] / 10000),
    sqrt(counts['10'] / 10000),
    sqrt(counts['11'] / 10000)
])

# statevector simulator
qc = create_qc()
result = execute(qc, statevector_sim).result()
v = result.get_statevector()
print('statevector simulator', [
    norm(v[0]), norm(v[1]), norm(v[2]), norm(v[3])
])
