import numpy as np

# Target unitary matrix (arbitrary example from the question)
U = np.array([[np.sqrt(1/5), np.sqrt(4/5)],
              [-np.sqrt(4/5), np.sqrt(1/5)]])

# There is no systematic way here to obtain theta, phi, lambda for U3
# so they are just guessed / left as placeholders.
theta = 0.0
phi = 0.0
lam = 0.0

def u3_matrix(theta, phi, lam):
    return np.array([
        [np.cos(theta / 2), -np.exp(1j * lam) * np.sin(theta / 2)],
        [np.exp(1j * phi) * np.sin(theta / 2),
         np.exp(1j * (lam + phi)) * np.cos(theta / 2)]
    ])

guessed = u3_matrix(theta, phi, lam)
print("Guessed U3 matrix:")
print(guessed)
print("Target matrix:")
print(U)
