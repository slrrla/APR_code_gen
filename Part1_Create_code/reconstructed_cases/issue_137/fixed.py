from qiskit import QuantumCircuit, execute
from qiskit.providers.aer import AerSimulator

# Build a simple circuit
qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

# The reported error is not a code bug: it is caused by a local network
# tool (safebrowse.io) blocking the IBM Cloud object storage URL used by
# IBMQ job submission, which results in SSL "Max retries exceeded" errors.
# The real fix is to disable safebrowse.io on the client machine, not to
# change the Qiskit code. Here we substitute a local simulator so the
# circuit still runs without depending on network access to IBMQ.
backend = AerSimulator()

job = execute(qc, backend=backend, shots=1024)
result = job.result()
print(result.get_counts(qc))
