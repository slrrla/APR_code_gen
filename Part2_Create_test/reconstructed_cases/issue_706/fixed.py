import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit.primitives import Sampler, Estimator

observable = SparsePauliOp.from_list([("X", 1), ("Z", 1)])
circuit = QuantumCircuit(1)
circuit.ry(np.pi / 2, 0)  # use Ry instead of Rx to correctly prepare |+>

cir = circuit.copy()
cir.measure_all()
sampler = Sampler()
job = sampler.run(cir)
probabilities = job.result().quasi_dists[0]
observableMat = observable.to_matrix()
probabilitiesAr = np.sqrt(
    np.array([probabilities.get(i, 0) for i in range(observable.num_qubits + 1)])
)
expectationValue = np.inner(np.conj(probabilitiesAr), np.dot(observableMat, probabilitiesAr))
print(expectationValue.real)  # outputs 1.0

estimator_result = Estimator().run(circuit, observable).result().values[0].real
print(estimator_result)  # outputs 1.0 now, matching the Sampler-based calculation
