# Imports
from math import pi
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Operator
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import EstimatorV2

# Create estimator object
backend = AerSimulator()
estimator = EstimatorV2(mode=backend)

# Define operator
O = Operator([[1,0,0,-2j],
              [0,0,0,0],
              [0,0,0,0],
              [2j,0,0,1]])

# Use the Operator directly as observable (not supported by Estimator)
obs = O

# create quantum circuit
qc = QuantumCircuit(2)
qc.rx(pi/3,1)
qc.cx(1,0)

# transpile
qc_t = transpile(qc,backend)

# run simulation
job = estimator.run([(qc_t,[obs])])
exp_vals = job.result()[0].data.evs
print(exp_vals)
