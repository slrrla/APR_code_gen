import random
from qiskit import QuantumCircuit, execute, Aer

# Instead of measuring (which collapses the qubit), access the
# wavefunction directly with the statevector simulator, and
# manually simulate the observation postulate:
#   r <= |a|^2  -> x = 0  (basis state |0>)
#   r >  |a|^2  -> x = 1  (basis state |1>)

qc = QuantumCircuit(1)
qc.h(0)

backend = Aer.get_backend('statevector_simulator')
result = execute(qc, backend).result()

# Newer Qiskit API: use result.data() instead of result.get_data(circuit)
statevector = result.data()['statevector']

a = statevector[0]  # amplitude of |0>
prob0 = abs(a) ** 2

r = random.random()
if r <= prob0:
    x = 0
else:
    x = 1

print("Simulated observation (no collapse of the actual backend state):", x)
