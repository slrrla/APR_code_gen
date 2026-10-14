from qiskit.aqua.algorithms import Shor
from qiskit.aqua import QuantumInstance
from qiskit.test.mock import FakeMelbourne

PRIME = 15

backend = FakeMelbourne()
quantum_instance = QuantumInstance(backend, skip_qobj_validation=False)

shor = Shor(PRIME, 2)
res = shor.run(quantum_instance)
print("The list of factors of {} as computed by Shor is {}.".format(PRIME, res['factors'][0]))
