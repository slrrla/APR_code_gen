from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, execute, Aer
from qiskit.ignis.mitigation.measurement import (complete_meas_cal, CompleteMeasFitter)
import matplotlib.pyplot as plt

# 4-qubit circuit used to build the calibration matrix
qr = QuantumRegister(4)
cr = ClassicalRegister(4)
qc = QuantumCircuit(qr, cr)

backend = Aer.get_backend('qasm_simulator')

cal_circuits, state_labels = complete_meas_cal(qr=qc.qregs[0], circlabel='measerrormitigationcal')
cal_job = execute(cal_circuits, backend=backend, shots=1024, optimization_level=0)
print(cal_job.job_id())
cal_results = cal_job.result()
meas_fitter = CompleteMeasFitter(cal_results, state_labels)

fig, ax = plt.subplots(figsize=(10, 10))
# FIX: derive a subset fitter for the 3 qubits of interest instead of
# reusing the full 4-qubit calibration matrix
subset_meas_fitter = meas_fitter.subset_fitter([0, 1, 2])  # defining new meas_fitter for a set of qubits
subset_meas_fitter.plot_calibration(ax)
