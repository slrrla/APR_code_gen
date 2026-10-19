from qiskit import QuantumCircuit
from qiskit.compiler import transpile
from qiskit.transpiler import PassManager, passes
from qiskit.test.mock import FakeMelbourne
# NB will need to install dev requirements

""" This is the circuit we are going to look at"""
qc = QuantumCircuit(13, 13)
qc.h(3)
qc.cx(0, 6)
qc.h(1)
qc.cx(6, 0)
qc.cx(0, 1)
qc.cx(3, 1)
qc.h(3)
qc.cx(3, 0)
qc.measure_all()

backend = FakeMelbourne()
properties = backend.properties()
coupling_map = backend.configuration().coupling_map
# No way is used here to actually obtain or display the logical->physical
# qubit mapping; the user is stuck with just the coupling map.
