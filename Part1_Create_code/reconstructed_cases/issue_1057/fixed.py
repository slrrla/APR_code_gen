import pennylane as qml
import numpy as np

def RXX(theta):
    rxx = np.array([
        [np.cos(theta/2), 0, 0, -1j*np.sin(theta/2)],
        [0, np.cos(theta/2), -1j*np.sin(theta/2), 0],
        [0, -1j*np.sin(theta/2), np.cos(theta/2), 0],
        [-1j*np.sin(theta/2), 0, 0, np.cos(theta/2)]
    ])
    return rxx

dev = qml.device('default.qubit', wires=2)

@qml.qnode(dev)
def circuit(theta):
    qml.QubitUnitary(RXX(theta), wires=[0, 1])
    return qml.expval(qml.PauliZ(0))

circuit(0.3)
