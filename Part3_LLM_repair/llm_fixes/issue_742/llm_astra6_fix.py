from math import pi
from qiskit import QuantumCircuit, transpile
# FIX: Operator alone is not accepted by EstimatorV2 -> import SparsePauliOp, because it provides a supported observable representation.
from qiskit.quantum_info import Operator, SparsePauliOp
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import EstimatorV2

backend = AerSimulator()
estimator = EstimatorV2(mode=backend)

O = Operator([[1,0,0,-2j],
              [0,0,0,0],
              [0,0,0,0],
              [2j,0,0,1]])

# FIX: The dense Operator is unsupported by EstimatorV2 -> decompose it with SparsePauliOp.from_operator, because this represents the same observable as a sum of Pauli words.
obs = SparsePauliOp.from_operator(O)

qc = QuantumCircuit(2)
qc.rx(pi/3,1)
qc.cx(1,0)

qc_t = transpile(qc,backend)

job = estimator.run([(qc_t,[obs])])
exp_vals = job.result()[0].data.evs
print(exp_vals)

