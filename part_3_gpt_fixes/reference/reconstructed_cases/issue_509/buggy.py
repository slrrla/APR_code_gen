import numpy as np

sig_z = np.array([[1, 0], [0, -1]])
# Bug: this is actually an Rz gate, not an Ry gate
rz = np.array([[np.exp(-1j*np.pi/4), 0], [0, np.exp(1j*np.pi/4)]])
print(np.matmul(rz, np.matmul(sig_z, -rz)))
