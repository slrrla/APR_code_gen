from qiskit import QuantumCircuit, transpile, Aer, IBMQ, QuantumRegister, ClassicalRegister, execute
import numpy as np

q = QuantumRegister(2)
c = ClassicalRegister(2)
circ = QuantumCircuit(q, c)

# Trying to prepare the state |11> by just defining the amplitude vector,
# but forgetting to actually apply it to the circuit.
state = np.array([0, 0, 0, 1])  # |11>
# BUG: circ.initialize(state) is never called, so the circuit stays in |00>

circ.measure(q, c)

processor = Aer.backends(name='qasm_simulator')[0]  # simulator
res = execute(circ, processor, shots=1).result().get_counts(circ)
print(res)
