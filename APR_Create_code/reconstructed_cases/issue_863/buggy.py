import numpy as np

swapcnot = np.array([[1, 0, 0, 0],
                      [0, 0, 0, 1],
                      [0, 0, 1, 0],
                      [0, 1, 0, 0]])

cnot = np.array([[1, 0, 0, 0],
                  [0, 1, 0, 0],
                  [0, 0, 0, 1],
                  [0, 0, 1, 0]])

layer1 = np.kron(np.eye(2), swapcnot)
layer2 = np.kron(swapcnot, np.eye(2))
layer3 = np.kron(np.eye(2), cnot)

print(layer3 @ layer2 @ layer1)
