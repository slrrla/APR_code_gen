import numpy as np
from qiskit.quantum_info import DensityMatrix, state_fidelity

# state1: a valid density matrix
state1 = DensityMatrix(np.array([[1, 0], [0, 0]]))

# state2: constructed from tomography expectation values,
# which may not correspond to a physically valid (positive semidefinite) state
expectation_vals = [0.004, 1.0, -0.04]

# Turn this into a density matrix
state2_matrix = (1/2)*np.array([[1+expectation_vals[0], expectation_vals[1]-1j*expectation_vals[2]],
                                 [expectation_vals[1]+1j*expectation_vals[2], 1-expectation_vals[0]]])
state2 = DensityMatrix(state2_matrix)

# Disable validation so fidelity can be computed even though state2
# is not a strictly valid quantum state
fidelity = state_fidelity(state1, state2, validate=False)
print(fidelity)
