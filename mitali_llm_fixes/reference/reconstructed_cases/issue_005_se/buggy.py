from qiskit import QuantumCircuit
from qiskit.utils import QuantumInstance
from qiskit.providers.aer import AerSimulator

backend = AerSimulator()
quantum_instance = QuantumInstance(backend, shots=1024)

qc = QuantumCircuit(1)
qc.h(0)
qc.measure_all()

result = quantum_instance.execute(qc)
print(result.get_counts())
