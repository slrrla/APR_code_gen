import qiskit
from qiskit import execute, Aer
from qiskit.ignis.mitigation.measurement import (complete_meas_cal,
                                                   CompleteMeasFitter)

# Local simulator stands in for the real device (no network calls)
backend = Aer.get_backend('qasm_simulator')

# Generate the calibration circuits
qr = qiskit.QuantumRegister(4)
meas_calibs, state_labels = complete_meas_cal(qr=qr, circlabel='mcal')

# Bug: try to run ALL calibration circuits in a single job without
# splitting them into batches, which fails on real hardware because
# the number of experiments exceeds the device's supported limit.
job = execute(meas_calibs, backend=backend, shots=1024, optimization_level=0)
result = job.result()

meas_fitter = CompleteMeasFitter(result, state_labels, circlabel='mcal')
meas_fitter.plot_calibration()
