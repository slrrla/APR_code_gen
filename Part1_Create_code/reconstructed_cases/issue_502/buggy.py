from qiskit.providers.aer.noise.errors import (
    pauli_error,
    depolarizing_error,
    phase_damping_error,
    amplitude_damping_error,
)

# Arbitrary, unrelated probabilities used to compare pauli_error vs depolarizing_error
p_x, p_y, p_z = 0.1, 0.2, 0.3
error1 = pauli_error([('X', p_x), ('Y', p_y), ('Z', p_z), ('I', 1 - p_x - p_y - p_z)])

p = 0.3
error2 = depolarizing_error(p, 1)

print(error1)
print(error2)

gamma = 0.1
error3 = phase_damping_error(gamma)
error4 = amplitude_damping_error(gamma)
print(error3)
print(error4)
