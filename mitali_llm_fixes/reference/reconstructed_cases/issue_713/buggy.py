from qiskit import QuantumCircuit, execute
from qiskit import Aer

qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

# Local Aer simulator - runs on the user's own CPU, does NOT show up
# as a job in the IBM Q "Jobs" pane.
processor = Aer.backends(name='qasm_simulator')[0]

job = execute(qc, backend=processor, shots=1024)
result = job.result()
print(result.get_counts(qc))
