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

### Bridge Gate part of the circuit ####
layer3 = np.kron(np.eye(2), cnot)
layer4 = np.kron(cnot, np.eye(2))
layer5 = np.kron(np.eye(2), cnot)
layer6 = np.kron(cnot, np.eye(2))
####################################

print(layer6 @ layer5 @ layer4 @ layer3 @ layer2 @ layer1)
