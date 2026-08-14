from qiskit import Aer
from qiskit.algorithms import Shor
from qiskit.utils import QuantumInstance

# Attempt to factor N=33 using base a=2.
# For N=33, a=2 fails because 2^5 = 32 = -1 (mod 33),
# so the period-finding never yields a usable factor.
N = 33
a = 2

backend = Aer.get_backend('qasm_simulator')
quantum_instance = QuantumInstance(backend, shots=1000)

shor = Shor(quantum_instance=quantum_instance)
result = shor.factor(N=N, a=a)

print("Factors found:", result.factors)
