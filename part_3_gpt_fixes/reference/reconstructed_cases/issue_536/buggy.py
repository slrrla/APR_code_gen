import pennylane as qml
from pennylane import numpy as np

# n_wires is created as a trainable tensor instead of a plain int.
# This makes the device's wire labels tensors, causing a mismatch
# with the plain integer wires used inside the circuit.
n_wires = np.tensor(18, requires_grad=True)

dev = qml.device("qiskit.aer", shots=1000, wires=n_wires)

@qml.qnode(dev)
def test(wires):
    qml.Hadamard(wires=wires[0])
    return [qml.expval(qml.PauliZ(i)) for i in range(n_wires)]

wires = range(n_wires)
test(wires)
