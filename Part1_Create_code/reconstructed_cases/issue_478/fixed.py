from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime.fake_provider import FakeBrisbane
from mthree import M3Mitigation
import mthree.utils as mutils
import json

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
m3_mitigator.cals_from_system(meas_mapping)

# Save calibration data and measurement mapping so they can be reused later
m3_mitigator.cals_to_file('calibration_data.json')
with open('measurement_mapping.json', 'w') as f:
    json.dump(meas_mapping, f)

max_shots = 1000
job = fake_be.run(transpiled_qc, shots=max_shots)
print(job.job_id())

result = job.result()
counts = result.get_counts()

# Reload calibration data and measurement mapping, then apply correction
m3_mitigator_loaded = M3Mitigation()
m3_mitigator_loaded.cals_from_file('calibration_data.json')
with open('measurement_mapping.json', 'r') as f:
    meas_mapping_loaded = json.load(f)

mitigated_counts = m3_mitigator_loaded.apply_correction(counts, meas_mapping_loaded)
print(mitigated_counts)
