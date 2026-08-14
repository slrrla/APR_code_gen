from qiskit import Aer
from qiskit.algorithms import Shor
from qiskit.utils import QuantumInstance

# Attempt to factor N=33 using base a=5 instead of a=2.
# a=5 does not satisfy a^(r/2) = -1 (mod N) for any r,
# so the period-finding succeeds and factors are returned.
N = 33
a = 5

backend = Aer.get_backend('qasm_simulator')
quantum_instance = QuantumInstance(backend, shots=1000)

shor = Shor(quantum_instance=quantum_instance)
result = shor.factor(N=N, a=a)

print("Factors found:", result.factors)
