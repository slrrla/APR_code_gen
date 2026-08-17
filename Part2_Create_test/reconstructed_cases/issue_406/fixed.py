import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, Operator

# Build an example state |x> (as produced by some algorithm, e.g. HHL)
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
x = Statevector.from_instruction(qc)

N = 2 ** x.num_qubits

# Correct observable: M = |+><+|, the projector onto the uniform superposition
plus = np.ones(N) / np.sqrt(N)
M = Operator(np.outer(plus, plus))

exp_val = x.expectation_value(M)

# Recover the absolute average from <x|M|x> = (1/N)|sum(x_i)|^2
absolute_average = np.sqrt(exp_val.real / N)

print("Absolute average (correct observable):", absolute_average)
