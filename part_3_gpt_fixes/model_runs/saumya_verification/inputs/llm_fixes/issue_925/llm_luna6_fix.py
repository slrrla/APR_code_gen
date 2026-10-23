from qiskit.aqua.algorithms import Shor
from qiskit.aqua import QuantumInstance
# FIX: FakeMelbourne has only 15 qubits -> use 20-qubit FakeTokyo, because Shor's circuit needs 18 qubits.
from qiskit.test.mock import FakeTokyo

PRIME = 15

# FIX: FakeMelbourne cannot run the 18-qubit circuit -> use FakeTokyo, because it has enough qubits.
backend = FakeTokyo()
quantum_instance = QuantumInstance(backend, skip_qobj_validation=False)

shor = Shor(PRIME, 2)
res = shor.run(quantum_instance)
print("The list of factors of {} as computed by Shor is {}.".format(PRIME, res['factors'][0]))

