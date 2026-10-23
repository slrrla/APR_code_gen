# FIX: The import list lacked numpy, which is needed for pi -> added numpy import, because the global phase update below uses np.pi
import numpy as np
from qiskit import QuantumCircuit

qc = QuantumCircuit(2)
qc.h([0, 1])

gate1 = qc.h
# FIX: `-1 * gate1` multiplied a bound method by -1 and never changed the circuit -> add pi to the circuit's global phase, because multiplying a unitary by -1 is a global phase of pi
qc.global_phase += np.pi
