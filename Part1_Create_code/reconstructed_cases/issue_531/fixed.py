from pyquil import *
from pyquil.gates import *
from qiskit import QuantumCircuit, execute
from qiskit_rigetti import RigettiQCSProvider

qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

# Increase execution_timeout to avoid "Timeout on client tcp://127.0.0.1:5555" error
provider = RigettiQCSProvider(execution_timeout=60)
backend = provider.get_backend(name="Aspen-11")

job = execute(qc, backend)
