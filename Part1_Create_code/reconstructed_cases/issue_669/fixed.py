from qiskit import QuantumCircuit
from qiskit.providers.aer.library import SaveStatevector
from qiskit import Aer
import numpy as np

# prepare a simple statevector to initialize with
psi = np.array([1, 0, 0, 1]) / np.sqrt(2)

qc = QuantumCircuit(2)
qc.initialize(psi, [0, 1])

qc2 = qc
qc2 = qc2.decompose(reps=20)

num_qubits = qc2.num_qubits
for index in range(len(qc2.data) - 1, -1, -1):
    _inst = SaveStatevector(num_qubits, label='psi_' + str(index))
    qc2.data.insert(index, [_inst, qc2.qubits, None])

simulator = Aer.get_backend('qasm_simulator')
result = simulator.run(qc2).result()
for key, value in result.data().items():
    print(key)
    print(value)
