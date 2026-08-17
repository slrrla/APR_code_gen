import numpy
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.quantum_info import Operator

# Placeholder standing in for the BQSKIT compiled circuit approximation
def bqskit_to_qiskit(circuit):
    return circuit

out_circuit = QuantumCircuit(3)
out_circuit.h(0)
out_circuit.t(0)
out_circuit.h(0)
out_circuit.ccx(0, 1, 2)

qc = bqskit_to_qiskit(out_circuit)
op = Operator(qc)
testVector = Statevector(QuantumCircuit(3))
print('Exact:', numpy.real_if_close(testVector.expectation_value(op)))
