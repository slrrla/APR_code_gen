from qiskit import QuantumCircuit, BasicAer, execute

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

backend = BasicAer.get_backend('qasm_simulator')

# Trying to use Aer-style simulation methods with BasicAer,
# which does not support them.
job = execute(qc, backend, backend_options={'method': 'statevector'})
result = job.result()
print(result.get_counts())
