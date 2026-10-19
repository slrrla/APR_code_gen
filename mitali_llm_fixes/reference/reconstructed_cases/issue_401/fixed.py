from qiskit import QuantumCircuit, execute
from qiskit.providers.aer import AerSimulator

# Fix: use a spin-echo style bit-flip in the middle of the wait time.
# Waiting time t is split into t/2, a bit flip, then t/2, then another
# bit flip. This swaps the roles of |0> and |1> for half the wait time
# so the accumulated relative phases cancel out, avoiding the
# spurious measurement of |1> after HH.

qc = QuantumCircuit(1, 1)
qc.h(0)
qc.delay(250, 0, unit='dt')
qc.x(0)
qc.delay(250, 0, unit='dt')
qc.x(0)
qc.h(0)
qc.measure(0, 0)

backend = AerSimulator()
result = execute(qc, backend, shots=1024).result()
counts = result.get_counts()
print(counts)
