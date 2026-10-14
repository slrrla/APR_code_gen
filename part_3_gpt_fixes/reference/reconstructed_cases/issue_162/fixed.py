from qiskit import QuantumCircuit, BasicAer, execute

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

# Check which backends BasicAer actually provides
print(BasicAer.backends())

for backend in BasicAer.backends():
    print("%s: %s" % (backend.name(), backend.__doc__))

backend = BasicAer.get_backend('qasm_simulator')

job = execute(qc, backend)
result = job.result()
print(result.get_counts())
