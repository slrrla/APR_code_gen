from qiskit import QuantumCircuit
from qiskit.extensions import Initialize
from qiskit.quantum_info import random_statevector
from IPython.display import display

# Create a sample 2-qubit circuit:
circ = QuantumCircuit(2)
circ.h(0)
circ.cx(0, 1)

# Repeatedly initialize the circuit with a random quantum state:
for m in range(5):
    # Create a 2-qubit random statevector:
    state = random_statevector(2 ** 2)
    # Create an "Initialize" instruction and prepend it to the circuit:
    new_circ = circ.compose(Initialize(state), front=True, inplace=False)
    print('Circuit No.', m + 1)
    display(new_circ.draw(fold=-1))
