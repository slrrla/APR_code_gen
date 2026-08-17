import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, Operator

# Build an example state |x> (as produced by some algorithm, e.g. HHL)
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
x = Statevector.from_instruction(qc)

N = 2 ** x.num_qubits

# Guessed (incorrect) observable M to extract the absolute average of x
# Using a plain Z-type operator instead of the |+><+| projector
M = Operator(np.diag([1, -1, -1, 1]))

exp_val = x.expectation_value(M)

# Attempt to recover the absolute average from <x|M|x>
absolute_average = np.sqrt(exp_val.real / N)

print("Absolute average (buggy observable):", absolute_average)
