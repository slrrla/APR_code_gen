from qiskit.providers.aer.noise.errors import (
    pauli_error,
    depolarizing_error,
    phase_damping_error,
    amplitude_damping_error,
)

# depolarizing_error(p, 1) is the special case of pauli_error where p_x = p_y = p_z = p/3
p = 0.3
p_x = p_y = p_z = p / 3
error1 = pauli_error([('X', p_x), ('Y', p_y), ('Z', p_z), ('I', 1 - p_x - p_y - p_z)])

error2 = depolarizing_error(p, 1)

print(error1)
print(error2)

gamma = 0.1
error3 = phase_damping_error(gamma)
error4 = amplitude_damping_error(gamma)
print(error3)
print(error4)
