from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram

qc = QuantumCircuit(4)
qc.h(range(4))
num_iterations = 16  # Set the number of iterations

# Oracle for marking |01> state
oracle = QuantumCircuit(4)
oracle.x(0)
oracle.x(2)
oracle.cx([0, 1, 2], 3)
oracle.x(0)
oracle.x(2)

# Grover diffusion operator
grover_diffusion = QuantumCircuit(4)
grover_diffusion.h(range(4))
grover_diffusion.z(3)
grover_diffusion.cz([0, 1, 2], 3)
grover_diffusion.h(range(3))

# Apply the oracle and Grover diffusion iteratively
for _ in range(num_iterations):
    qc.compose(oracle, inplace=True)
    # Apply the Grover diffusion operator
    qc.compose(grover_diffusion, inplace=True)

sv_sim = Aer.get_backend('statevector_simulator')
result = sv_sim.run(qc).result()
statevec = result.get_statevector()

from qiskit.visualization import array_to_latex
array_to_latex(statevec, prefix="|\\psi\\rangle =")

# Measure circuit
measurer = QuantumCircuit(4, 3)
measurer.measure([0, 1, 2], [0, 1, 2])
qc.compose(measurer, inplace=True)
# Measure the qubits
# qc.measure([0,1,2],[0,1,2])

qasm_sim = Aer.get_backend('qasm_simulator')
result = qasm_sim.run(qc).result()
counts = result.get_counts()
plot_histogram(counts)
