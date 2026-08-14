import numpy as np
import qiskit as qk
from qiskit import QuantumCircuit

# Stand-in for the external `_get_measurement_circuit` from the referenced
# GitHub repository, reproducing the circuit shown for this stabilizer matrix.
def _get_measurement_circuit(stabilizer_matrix, n):
    circ = QuantumCircuit(n)
    circ.cz(0, 1)
    circ.h(0)
    circ.s(1)
    circ.h(1)

    class MeasurementCircuit:
        pass

    mc = MeasurementCircuit()
    mc.circuit = circ
    return mc

sigmax = np.array([[0, 1], [1, 0]])
sigmay = np.array([[0, -1j], [1j, 0]])
sigmaz = np.array([[1, 0], [0, -1]])
id2 = np.identity(2)

n = 2
stabilizer_matrix = np.array([[0, 1], [1, 1], [1, 0], [0, 1]])
measurement_circuit = _get_measurement_circuit(stabilizer_matrix, n)  # this is the function from the quoted github
circ = measurement_circuit.circuit

backend = qk.Aer.get_backend('unitary_simulator')
job = qk.execute(circ, backend)
result = job.result()
U = result.get_unitary(circ, decimals=3)
U_GC1 = np.array(U)
print(U_GC1)

family_GC1 = [np.kron(sigmax, sigmaz), np.kron(sigmaz, sigmay), np.kron(sigmay, sigmax)]
for op in family_GC1:
    print(np.transpose(U_GC1 @ op @ np.transpose(U_GC1.conj())))
