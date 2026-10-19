import qiskit
from qiskit import execute, Aer
from qiskit.ignis.mitigation.measurement import (complete_meas_cal,
                                                   CompleteMeasFitter)

# Local simulator stands in for the real device (no network calls)
backend = Aer.get_backend('qasm_simulator')

# Generate the calibration circuits
qr = qiskit.QuantumRegister(4)
meas_calibs, state_labels = complete_meas_cal(qr=qr, circlabel='mcal')

# Split calibration circuits into two batches
job1_res = execute(meas_calibs[0:8], backend=backend, shots=1024,
                    optimization_level=0).result()
job2_res = execute(meas_calibs[8:16], backend=backend, shots=1024,
                    optimization_level=0).result()

# Initialize the measurement correction fitter with the first 8 calibration circuits
meas_fitter = CompleteMeasFitter(job1_res, state_labels, circlabel='mcal')
meas_fitter.plot_calibration()

# Update the measurement correction fitter with the second 8 calibration circuits
meas_fitter.add_data(new_results=job2_res)
meas_fitter.plot_calibration()
