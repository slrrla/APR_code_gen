# FIX: missing numpy import for np.pi -> added import numpy as np, because the global phase fix needs np.pi
import numpy as np
from qiskit import QuantumCircuit

qc = QuantumCircuit(2)
qc.h([0, 1])

gate1 = qc.h
# FIX: -1 * bound method is invalid (TypeError) and does nothing -> apply a global phase of pi, because multiplying an operator by -1 is exactly e^{i*pi}
qc.global_phase += np.pi
