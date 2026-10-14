from math import pi
from qiskit import QuantumCircuit, transpile
# FIX: Operator alone cannot provide the required Pauli decomposition -> import SparsePauliOp, because EstimatorV2 accepts Pauli-based observables.
from qiskit.quantum_info import Operator, SparsePauliOp
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import EstimatorV2

backend = AerSimulator()
estimator = EstimatorV2(mode=backend)

O = Operator([[1,0,0,-2j],
              [0,0,0,0],
              [0,0,0,0],
              [2j,0,0,1]])

# FIX: A general Operator is not a supported EstimatorV2 observable -> decompose it with SparsePauliOp.from_operator, because this preserves the operator in a supported representation.
obs = SparsePauliOp.from_operator(O)

qc = QuantumCircuit(2)
qc.rx(pi/3,1)
qc.cx(1,0)

qc_t = transpile(qc,backend)

job = estimator.run([(qc_t,[obs])])
exp_vals = job.result()[0].data.evs
print(exp_vals)
