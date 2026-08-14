from qiskit import QuantumCircuit, execute
from qiskit import IBMQ

qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

# Cloud-hosted simulator - runs on IBM's servers and shows up as a
# job in the IBM Q "Jobs" pane, just like a real device would.
provider = IBMQ.load_account()
processor = provider.backends(name='ibmq_qasm_simulator')[0]

job = execute(qc, backend=processor, shots=1024)
result = job.result()
print(result.get_counts(qc))
