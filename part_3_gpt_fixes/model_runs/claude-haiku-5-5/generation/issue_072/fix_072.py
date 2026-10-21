import qiskit as qk
from qiskit import Aer
from qiskit.ignis.mitigation.measurement import complete_meas_cal

_backend = Aer.get_backend('qasm_simulator')

qreg = qk.QuantumRegister(7)
# FIX: qreg[5] and qreg[0] both mapped to physical qubit 12 (duplicate in layout) -> remapped qreg[5] to unused physical qubit 0, because each virtual qubit must map to a unique physical qubit for transpile to succeed
layout = {qreg[0]: 12, qreg[1]: 11, qreg[2]: 13, qreg[3]: 17, qreg[4]: 14, qreg[5]: 0, qreg[6]: 6}

meas_calibs, state_labels = complete_meas_cal(
    qubit_list=[0, 1, 2], qr=qreg, circlabel='mcal')
print(meas_calibs[0])
qk.compiler.transpile(meas_calibs, backend=_backend, initial_layout=layout)
