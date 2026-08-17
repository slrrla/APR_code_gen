from pyquil import *
from pyquil.gates import *
from qiskit import QuantumCircuit, execute
from qiskit_rigetti import RigettiQCSProvider

qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

# Timeout occurs on large circuits because default execution_timeout is too short
provider = RigettiQCSProvider()
backend = provider.get_backend(name="Aspen-11")

job = execute(qc, backend)
