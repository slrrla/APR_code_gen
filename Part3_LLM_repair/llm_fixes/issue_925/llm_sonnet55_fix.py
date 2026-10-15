from qiskit.aqua.algorithms import Shor
from qiskit.aqua import QuantumInstance
# FIX: imported the FakeMelbourne mock (15 qubits) -> import Aer instead, because the Shor circuit for N=15 needs 18 qubits and only a simulator can run it
from qiskit import Aer

PRIME = 15

# FIX: used a 15-qubit device backend -> use the Aer qasm_simulator, because the 18-qubit circuit exceeds the device's coupling map
backend = Aer.get_backend('qasm_simulator')
quantum_instance = QuantumInstance(backend, skip_qobj_validation=False)

shor = Shor(PRIME, 2)
res = shor.run(quantum_instance)
print("The list of factors of {} as computed by Shor is {}.".format(PRIME, res['factors'][0]))
