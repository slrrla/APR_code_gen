import numpy as np
from qiskit import QuantumCircuit

def cnx(qc, *qubits):
    if len(qubits) >= 3:
        last = qubits[-1]
        # What is the goal of the next two lines?
        qc.crz(np.pi/2, qubits[-2], qubits[-1])
        qc.cry(np.pi/2, 0, 0, qubits[-2], qubits[-1])
        # Is this a recursive call to cnx?
        cnx(qc, *qubits[:-2], qubits[-1])
        # why is there another flip?
        qc.cry(-np.pi/2, 0, 0, qubits[-2], qubits[-1])
        # what about this line?
        cnx(qc, *qubits[:-2], qubits[-1])
        # what about this line too?
        qc.crz(-np.pi/2, qubits[-2], qubits[-1])

qc = QuantumCircuit(4)
cnx(qc, 0, 1, 2, 3)
print(qc)
