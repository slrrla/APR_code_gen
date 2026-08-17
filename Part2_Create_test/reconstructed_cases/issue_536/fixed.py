import pennylane as qml
from pennylane import numpy as np

# Use a plain integer for the number of wires so the device's wire
# labels are simple ints, matching the integer wires used in the circuit.
n_wires = 18

dev = qml.device("qiskit.aer", shots=1000, wires=n_wires)

@qml.qnode(dev)
def test(wires):
    qml.Hadamard(wires=wires[0])
    return [qml.expval(qml.PauliZ(i)) for i in range(n_wires)]

wires = range(n_wires)
test(wires)
