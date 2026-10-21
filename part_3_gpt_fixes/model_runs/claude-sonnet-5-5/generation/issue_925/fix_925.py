from qiskit.aqua.algorithms import Shor
from qiskit.aqua import QuantumInstance
from qiskit import Aer

PRIME = 15

# FIX: used a 15-qubit FakeMelbourne backend, but Shor for N=15 needs 18 qubits -> use the Aer qasm_simulator, because it has enough qubits to run the circuit
backend = Aer.get_backend('qasm_simulator')
quantum_instance = QuantumInstance(backend, skip_qobj_validation=False)

shor = Shor(PRIME, 2)
res = shor.run(quantum_instance)
print("The list of factors of {} as computed by Shor is {}.".format(PRIME, res['factors'][0]))
