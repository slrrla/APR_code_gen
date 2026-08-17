from qiskit import QuantumCircuit
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
    # Try to initialize the circuit directly - this mutates circ in place
    # and accumulates instructions on every iteration instead of producing
    # a fresh circuit with just the new initialization prepended.
    circ.initialize(state, [0, 1])
    print('Circuit No.', m + 1)
    display(circ.draw(fold=-1))
