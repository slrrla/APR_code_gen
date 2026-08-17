import numpy as np
from qiskit import Aer, QuantumCircuit, QuantumRegister
from qiskit.aqua.algorithms import IterativeAmplitudeEstimation
from qiskit.circuit.library import LogNormalDistribution, IntegerComparator

num_uncertainty_qubits = 3
S = 100
vol = 0.4
r = 0.04
T = 3 * (30 / 365)
mu = np.log(S) + (r - 0.5 * vol ** 2) * T
sigma = vol * np.sqrt(T)
mean = np.exp(mu - 0.5 * sigma ** 2)
variance = (np.exp(sigma ** 2) - 1) * np.exp(2 * mu + sigma ** 2)
stddev = np.sqrt(variance)
low = np.maximum(0, mean - 3 * stddev)
high = mean + 3 * stddev

uncertainty_model = LogNormalDistribution(num_uncertainty_qubits, mu=mu, sigma=sigma ** 2, bounds=(low, high))
# 3 qubit LogNormalDistribution model
uncertainty_model = LogNormalDistribution(3, mu=mu, sigma=sigma, bounds=(low, high))


def get_cdf_circuit(x_eval):
    qr_state = QuantumRegister(uncertainty_model.num_qubits, 'state')
    qr_obj = QuantumRegister(1, 'obj')
    qr_comp = QuantumRegister(2, 'compare')
    state_preparation = QuantumCircuit(qr_state, qr_obj, qr_comp)
    state_preparation.append(uncertainty_model, qr_state)
    comparator = IntegerComparator(uncertainty_model.num_qubits, x_eval, geq=False)
    state_preparation.append(comparator, qr_state[:] + qr_obj[:] + qr_comp[:])
    return state_preparation


def run_ae_for_cdf(x_eval, epsilon=0.01, alpha=0.05, simulator='qasm_simulator'):
    state_preparation = get_cdf_circuit(x_eval)
    # BUG: qr_state is a local variable inside get_cdf_circuit and is not
    # accessible here -> this reference is wrong / causes a NameError,
    # or (if a stray global exists) silently uses the wrong qubit index,
    # producing the same amplitude estimate regardless of x_eval.
    ae_var = IterativeAmplitudeEstimation(
        state_preparation=state_preparation,
        epsilon=epsilon,
        alpha=alpha,
        objective_qubits=[len(qr_state)]
    )
    result_var = ae_var.run(quantum_instance=Aer.get_backend(simulator), shots=100)
    return result_var['estimation']


print(run_ae_for_cdf(mean))
