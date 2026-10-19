import numpy as np

sig_z = np.array([[1, 0], [0, -1]])
# Use the correct Ry(pi/2) and Ry(-pi/2) matrices
ry_plus = np.array([[np.cos(np.pi/4), -np.sin(np.pi/4)],
                     [np.sin(np.pi/4), np.cos(np.pi/4)]])
ry_minus = np.array([[np.cos(-np.pi/4), -np.sin(-np.pi/4)],
                      [np.sin(-np.pi/4), np.cos(-np.pi/4)]])
print(np.matmul(ry_plus, np.matmul(sig_z, ry_minus)))
