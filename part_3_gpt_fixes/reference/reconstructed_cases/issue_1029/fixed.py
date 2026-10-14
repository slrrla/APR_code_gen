from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.visualization import array_to_latex
import pylab as plt

num_qubits = 13
circuit = QuantumCircuit(num_qubits)
for q in range(num_qubits):
    circuit.h(q)

# Remove any final measurements before building the Statevector
qc = circuit.remove_final_measurements(inplace=False)

# Show the full statevector amplitudes (careful: 2**13 entries)
array_to_latex(Statevector(qc), max_size=2**num_qubits)

# Alternatively, visualize the probability distribution as a histogram
x = range(2**num_qubits)
p = Statevector(qc).probabilities()
plt.bar(x=x, height=p)
plt.show()
