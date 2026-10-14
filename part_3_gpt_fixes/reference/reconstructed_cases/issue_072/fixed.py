import qiskit as qk
from qiskit import Aer
from qiskit.ignis.mitigation.measurement import complete_meas_cal

_backend = Aer.get_backend('qasm_simulator')

qreg = qk.QuantumRegister(7)
# qreg[5] no longer maps to the same physical qubit (12) as qreg[0]
layout = {qreg[0]: 12, qreg[1]: 11, qreg[2]: 13, qreg[3]: 17, qreg[4]: 14, qreg[5]: 16, qreg[6]: 6}

########## error mitigation ##########
meas_calibs, state_labels = complete_meas_cal(
    qubit_list=[0, 1, 2], qr=qreg, circlabel='mcal')
print(meas_calibs[0])
# This line below is causing error if I add "initial_layout" in both qk.compiler.transpile and qk.execute
qk.compiler.transpile(meas_calibs, backend=_backend, initial_layout=layout)
