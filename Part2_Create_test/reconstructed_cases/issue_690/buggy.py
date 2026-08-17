from qiskit import IBMQ, Aer, QuantumCircuit, execute

# Case 3 from the question: measure qubit 0 first, then apply H to qubit 1
# The author expected this to be equivalent to multiplying by a fixed
# "collapse" matrix and getting a deterministic post-measurement state.
qc = QuantumCircuit(2, 2)
qc.h(0)
qc.h(1)
qc.measure(0, 0)   # collapse qubit 0 before further processing
qc.h(1)            # re-apply H on qubit 1 after the measurement
qc.measure(1, 1)

backend = Aer.get_backend('statevector_simulator')
job = execute(qc, backend)
result = job.result()
print('Statevector:', result.get_statevector())
