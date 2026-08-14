from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime.fake_provider import FakeBrisbane
from mthree import M3Mitigation
import mthree.utils as mutils

# Use a local fake backend instead of real hardware
fake_be = FakeBrisbane()

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

transpiled_qc = transpile(qc, fake_be)

# Get the final measurement mapping
meas_mapping = mutils.final_measurement_mapping(transpiled_qc)

m3_mitigator = M3Mitigation(fake_be)
# Runs calibration against the backend every time, never saved for reuse
m3_mitigator.cals_from_system(meas_mapping)

max_shots = 1000
job = fake_be.run(transpiled_qc, shots=max_shots)
print(job.job_id())  # only the job id is saved, calibration data is lost

result = job.result()
counts = result.get_counts()
# BUG: correction is never applied to the raw counts
print(counts)
