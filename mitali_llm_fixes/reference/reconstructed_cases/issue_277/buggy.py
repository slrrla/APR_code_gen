import mthree
from qiskit import QuantumCircuit, execute, Aer

# Build a simple 3-qubit circuit
qc = QuantumCircuit(3)
qc.h(0)
qc.cx(0, 1)
qc.cx(1, 2)
qc.measure_all()

backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend, shots=1000)
counts = job.result().get_counts()

# Set up M3 mitigation (assume calibration already loaded from a saved file)
m3_mitigator_loaded = mthree.M3Mitigation(backend)
m3_mitigator_loaded.cals_from_system(range(3))

meas_mapping_loaded = list(range(3))

mitigated_counts = m3_mitigator_loaded.apply_correction(counts, meas_mapping_loaded)
print("counts:", counts, "mitigated_counts:", mitigated_counts)
