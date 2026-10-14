from qiskit import QuantumCircuit, transpile
from qiskit_braket_provider import BraketProvider

provider = BraketProvider()
ionq = provider.get_backend("IonQ Device")

qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

tqc = transpile(qc, ionq)

job = ionq.run(tqc, shots=1024, memory=True)
job.status()
job.wait_for_final_state()
result = job.result()
m = job.result().get_memory(tqc)
print(m)
