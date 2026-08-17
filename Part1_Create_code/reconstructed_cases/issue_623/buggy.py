from qiskit import QuantumCircuit, QuantumRegister
from qiskit_ibm_runtime.fake_provider import FakeBrisbane

# The user only had fragments: T1, T2 time, APIs
# They wanted to know the actual execution time on real hardware
# but had no working code to get scheduling/duration or T1/T2 info.

backend = FakeBrisbane()

qr = QuantumRegister(1)
qc = QuantumCircuit(qr)
qc.sx(0)
qc.measure_all()

# Naively run the circuit without transpiling for the backend's ISA
# and without any schedule/duration calculation.
job = backend.run(qc)
result = job.result()
print(result)
