import numpy as np

swapcnot = np.array([[1, 0, 0, 0],
                      [0, 0, 0, 1],
                      [0, 0, 1, 0],
                      [0, 1, 0, 0]])

layer1 = np.kron(np.eye(2), swapcnot)
layer2 = np.kron(swapcnot, np.eye(2))

print(np.matmul(layer2, layer1))
