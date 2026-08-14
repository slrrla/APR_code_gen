from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

qc = QuantumCircuit(4)
qc.h([0, 1, 2, 3])
qc.cx(1, 3)
qc.cx(2, 0)
qc.measure_all()

sim = AerSimulator()
job = sim.run(qc, shots=1024)
res = job.result().get_counts()
print(res)

# No way to get partial (marginal) probabilities for just qubits 0 and 1
# The full counts dictionary contains all 4 qubits' outcomes together
new_counts = res  # missing marginalization
print(new_counts)
