from qiskit.circuit.library import RYGate

def ccry(qc, theta, control1, control2, controlled):
    qc.cry(theta/2, control2, controlled)
    qc.cx(control1, control2)
    qc.cry(-theta/2, control2, controlled)
    qc.cx(control1, control2)
    qc.cry(theta/2, control1, controlled)

a = 0.5
CCCRY = RYGate(a).control(3)

qc.append()
