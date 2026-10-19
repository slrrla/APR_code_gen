# Question: Is there a clear explanation of how optimization_level
# in qiskit's transpile() method affects the circuit?
# The user compares circuits transpiled at different optimization levels
# but sees no visible simplification difference.

from qiskit import QuantumCircuit, transpile
from qiskit.providers.aer import Aer

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.cx(0, 1)
qc.h(0)

backend = Aer.get_backend('qasm_simulator')

# Transpiling at various optimization levels, expecting to see
# mathematical simplification of gates, but the result looks the same.
for level in [0, 1, 2, 3]:
    transpiled = transpile(qc, backend=backend, optimization_level=level)
    print(f"optimization_level={level}")
    print(transpiled)
