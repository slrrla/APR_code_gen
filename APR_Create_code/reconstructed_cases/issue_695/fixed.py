# Portfolio Optimization example using qiskit_finance / qiskit_optimization
from qiskit_finance.applications.optimization import PortfolioOptimization
from qiskit_finance.data_providers import RandomDataProvider
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit.algorithms import QAOA
from qiskit.algorithms.optimizers import SLSQP
from qiskit.utils import QuantumInstance
from qiskit import Aer
import datetime
import numpy as np

# Number of stocks in the portfolio
num_assets = 21

data = RandomDataProvider(
    tickers=[f"TICKER{i}" for i in range(num_assets)],
    start=datetime.datetime(2016, 1, 1),
    end=datetime.datetime(2016, 1, 30),
    seed=42,
)
data.run()
mu = data.get_period_return_mean_vector()
sigma = data.get_period_return_covariance_matrix()

q = 0.5  # risk factor
budget = num_assets // 2
penalty = num_assets

portfolio = PortfolioOptimization(
    expected_returns=mu, covariances=sigma, risk_factor=q, budget=budget
)
qp = portfolio.to_quadratic_program()

# Using the Sequential Least Squares Programming optimizer
optimizer = SLSQP(maxiter=1000)

# Check how many qubits/variables the model actually needs and pick a
# backend/simulator that can handle that number of qubits, e.g. the
# qasm_simulator (or another IBM-provided simulator with enough qubits)
# rather than defaulting to statevector_simulator.
num_vars = qp.get_num_vars()
print(f"Number of variables/qubits required: {num_vars}")

backend = Aer.get_backend("qasm_simulator")
quantum_instance = QuantumInstance(backend=backend, shots=1024)

qaoa = QAOA(optimizer=optimizer, reps=3, quantum_instance=quantum_instance)
meo = MinimumEigenOptimizer(qaoa)

result = meo.solve(qp)
print(result)
