from qiskit import QuantumCircuit, execute
from qiskit import Aer
import numpy as np

data = np.array([-0.5, -0.2, -0.2, -0.6])
norm_data = np.linalg.norm(data)
normalized_data = data / norm_data

qasm_sim = Aer.get_backend('qasm_simulator')
statevector_sim = Aer.get_backend('statevector_simulator')

def create_qc():
    qc = QuantumCircuit(2, 2)
    qc.initialize(normalized_data, [0, 1])
    qc.h(0)
    qc.cx(0, 1)
    qc.x(0)
    qc.rx(-np.pi/10, 0)
    qc.ry(-np.pi/20, 1)
    return qc

# qasm simulator
circuit = create_qc()
circuit.measure([0, 1], [0, 1])
print(circuit)
result = execute(circuit, qasm_sim, shots=10000).result()
counts = result.get_counts(circuit)
final_result = []
for key in counts:
    final_result.append(np.sqrt(counts[key] / 10000))
print(final_result)

# statevector simulator
circuit2 = create_qc()
print(circuit2)
result2 = execute(circuit2, statevector_sim).result()
output_complex = result2.get_statevector(circuit2)
output_real = np.array(np.real(output_complex))
print("The output real =", output_real)
