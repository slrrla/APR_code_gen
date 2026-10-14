import numpy as np
import qiskit as q
from qiskit.circuit import Parameter
from qiskit.quantum_info import SparsePauliOp
from qiskit_machine_learning.neural_networks import EstimatorQNN
from qiskit.circuit.library import CUGate

params1 = [Parameter("input1"), Parameter("weight1")]
qc1 = q.QuantumCircuit(2)
qc1.h(0)
qc1.ry(params1[0], 0)
qc1.append(CUGate(params1[1], 0, 0, 0), [0, 1])
qc1.rx(params1[1], 0)

observable1 = SparsePauliOp.from_list([("Z" * qc1.num_qubits, 1)])

estimator_qnn = EstimatorQNN(
    circuit=qc1,
    observables=observable1,
    input_params=[params1[0]],
    weight_params=[params1[1]]
)

estimator_qnn_input = np.random.random(estimator_qnn.num_inputs)
estimator_qnn_weights = np.random.random(estimator_qnn.num_weights)
estimator_qnn_forward = estimator_qnn.forward(estimator_qnn_input, estimator_qnn_weights)
