from math import pi, sqrt
from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram

qc = QuantumCircuit(4)
qc.h(range(4))
# Fourth qubit in |-> state
qc.z(3)
num_iterations = int(pi * sqrt(2 ** 3) / 4)  # Set the number of iterations

# Oracle for marking |01> state
oracle = QuantumCircuit(4)
oracle.x(0)
oracle.x(2)
oracle.mcx([0, 1, 2], 3)
oracle.x(0)
oracle.x(2)

# Grover diffusion operator
# We still make it acting on 4 qubits so that we don't change the rest of the code, but
# we're leaving the fourth qubit alone.
grover_diffusion = QuantumCircuit(4)
grover_diffusion.h(range(3))
grover_diffusion.x(range(3))
# For some reason Aer doesn't like the ccz gate, so we build one from a ccx using the Z = HXH relation
# grover_diffusion.ccz(0, 1, 2)
grover_diffusion.h(2)
grover_diffusion.ccx(0, 1, 2)
grover_diffusion.h(2)
grover_diffusion.x(range(3))
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
