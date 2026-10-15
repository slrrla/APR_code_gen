# FIX: FakeMelbourne (15-qubit coupling map) is too small for the 18-qubit Shor circuit -> import BasicAer from qiskit instead, because BasicAer's qasm_simulator has no coupling-map limit
from qiskit import BasicAer
from qiskit.aqua.algorithms import Shor
from qiskit.aqua import QuantumInstance

PRIME = 15

# FIX: FakeMelbourne backend replaced with BasicAer qasm_simulator -> simulator has enough qubits for the circuit, because the transpiler no longer rejects the 18-qubit circuit
backend = BasicAer.get_backend('qasm_simulator')
quantum_instance = QuantumInstance(backend, skip_qobj_validation=False)

shor = Shor(PRIME, 2)
res = shor.run(quantum_instance)
print("The list of factors of {} as computed by Shor is {}.".format(PRIME, res['factors'][0]))
