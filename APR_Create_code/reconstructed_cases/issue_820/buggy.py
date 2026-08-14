# Measurement error mitigation using the deprecated qiskit.ignis module
from qiskit import QuantumCircuit, execute
from qiskit.providers.aer import QasmSimulator
from qiskit.ignis.mitigation.measurement import complete_meas_cal, CompleteMeasFitter

backend = QasmSimulator()

# Build calibration circuits for measurement error mitigation
qr = None  # placeholder, ignis will build its own registers internally
meas_calibs, state_labels = complete_meas_cal(qubit_list=[0, 1], qr=qr, circlabel='mcal')

cal_results = execute(meas_calibs, backend=backend, shots=1000).result()

meas_fitter = CompleteMeasFitter(cal_results, state_labels, circlabel='mcal')

# Simple circuit to be measurement-error-mitigated
qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

raw_results = execute(qc, backend=backend, shots=1000).result()

mitigated_results = meas_fitter.filter.apply(raw_results)
print(mitigated_results.get_counts())
