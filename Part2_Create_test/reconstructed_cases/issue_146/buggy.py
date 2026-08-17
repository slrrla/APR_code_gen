import numpy as np
from qiskit import QuantumCircuit, Aer, execute

psi = QuantumCircuit(5)
psi.ry(np.pi/4., 0)
psi.x(0)
psi.x(1)

psi2 = QuantumCircuit(5)
psi2.ry(np.pi/4., 0)
psi2.x(0)

def QuantumCircuits_Statevectors_AreEquals(QuantumCircuit1, QuantumCircuit2, QubitIndex):
    statevector1_arr = np.empty([1, 2]).astype(complex)
    statevector2_arr = np.empty([1, 2]).astype(complex)
    QuantumCircuit1.snapshot("qbsnap", qubits=[QubitIndex])
    QuantumCircuit2.snapshot("qbsnap", qubits=[QubitIndex])
    backend = Aer.get_backend('statevector_simulator')
    snapshot1 = execute(QuantumCircuit1, backend).result().data()['snapshots']['statevector']['qbsnap']
    snapshot2 = execute(QuantumCircuit2, backend).result().data()['snapshots']['statevector']['qbsnap']
    statevector1_arr[0][0] = snapshot1[0][0]
    statevector1_arr[0][1] = snapshot1[0][1]
    statevector2_arr[0][0] = snapshot2[0][0]
    statevector2_arr[0][1] = snapshot2[0][1]
    return np.array_equal(statevector1_arr, statevector2_arr)

result = QuantumCircuits_Statevectors_AreEquals(psi, psi2, 0)
print(result)
