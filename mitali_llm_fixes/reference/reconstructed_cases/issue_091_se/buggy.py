import numpy as np
from time import time
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit.primitives import Estimator
from qiskit.quantum_info import SparsePauliOp
from qiskit.algorithms import MinimumEigensolver, VQEResult
from qiskit.algorithms.optimizers import BOBYQA


class CustomVQE(MinimumEigensolver):
    def __init__(self, estimator, circuit, optimizer, callback=None):
        self._estimator = estimator
        self._circuit = circuit
        self._optimizer = optimizer
        self._callback = callback

    def compute_minimum_eigenvalue(self, operators, aux_operators=None):
        # Define objective function to classically minimize over
        def objective(x):
            # Execute job with estimator primitive
            job = self._estimator.run([self._circuit], [operators], [x])
            # Get results from jobs
            est_result = job.result()
            # Get the measured energy value
            value = est_result.values[0]
            # Save result information using callback function
            if self._callback is not None:
                self._callback(value)
            return value

        # Select an initial point for the ansatzs' parameters
        x0 = np.pi / 4 * np.random.rand(self._circuit.num_parameters)

        # Run optimization
        res = self._optimizer.minimize(objective, x0=x0, bounds=None)

        # Populate VQE result
        result = VQEResult()
        result.cost_function_evals = res.nfev
        result.eigenvalue = res.fun
        result.optimal_parameters = res.x
        return result


# Minimal setup to reproduce the failure
theta = Parameter("theta")
circuit = QuantumCircuit(2)
circuit.h(0)
circuit.cx(0, 1)
circuit.rz(theta, 0)

ham_16 = SparsePauliOp.from_list([("ZZ", 1.0), ("XX", 0.5)])

estimator = Estimator()
optimizer = BOBYQA(maxiter=100)
custom_vqe = CustomVQE(estimator, circuit, optimizer)

start = time()
result = custom_vqe.compute_minimum_eigenvalue(ham_16)
end = time()

print(result)
