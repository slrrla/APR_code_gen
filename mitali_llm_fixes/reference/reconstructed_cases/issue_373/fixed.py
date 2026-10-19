from qiskit import QuantumCircuit, transpile
from qiskit.providers.aer import AerSimulator

device = AerSimulator()

for q3210 in ['0000', '0010', '0001', '0011']:
    qc = QuantumCircuit(4, 2)
    qc.initialize(q3210, qc.qubits)
    qc.cx(1, 2)
    qc.cx(0, 2)
    qc.ccx(0, 1, 3)
    qc.measure([2, 3], [0, 1])
    transpiled_qc = transpile(qc, device, optimization_level=3)
    job = device.run(transpiled_qc)
    result = job.result()
    print(q3210, " : ", result.get_counts())
