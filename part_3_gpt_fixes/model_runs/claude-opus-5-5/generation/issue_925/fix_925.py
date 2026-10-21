from qiskit.aqua.algorithms import Shor
from qiskit.aqua import QuantumInstance
from qiskit.test.mock import FakeMelbourne
# FIX: no simulator import was available -> import BasicAer, because the circuit must run on a backend without a 15-qubit limit
from qiskit import BasicAer

PRIME = 15

# FIX: FakeMelbourne (15 qubits) cannot host Aqua's Shor circuit, which needs 4n+2 = 18 qubits for N=15 -> use the qasm_simulator, because it has no coupling-map size limit
backend = BasicAer.get_backend('qasm_simulator')
quantum_instance = QuantumInstance(backend, skip_qobj_validation=False)

shor = Shor(PRIME, 2)
res = shor.run(quantum_instance)
print("The list of factors of {} as computed by Shor is {}.".format(PRIME, res['factors'][0]))
