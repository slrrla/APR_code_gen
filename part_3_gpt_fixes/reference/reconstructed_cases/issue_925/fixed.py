from qiskit.aqua.algorithms import Shor
from qiskit.aqua import QuantumInstance
from qiskit import Aer

PRIME = 15

# Use a local simulator with no artificial qubit/coupling-map limit,
# since Shor's circuit for N=15 actually needs 4n+2 qubits (18 here),
# not the 2n+3 quoted from the paper.
backend = Aer.get_backend('qasm_simulator')
quantum_instance = QuantumInstance(backend, skip_qobj_validation=False)

shor = Shor(PRIME, 2)
res = shor.run(quantum_instance)
print("The list of factors of {} as computed by Shor is {}.".format(PRIME, res['factors'][0]))
