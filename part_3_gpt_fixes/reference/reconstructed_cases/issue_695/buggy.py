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

# Number of stocks in the portfolio - works fine with 10, hangs with 21
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

# No consideration is given to how many qubits this backend can actually handle
# for the number of variables/qubits required (21 stocks -> 21+ qubits).
backend = Aer.get_backend("statevector_simulator")
quantum_instance = QuantumInstance(backend=backend)

qaoa = QAOA(optimizer=optimizer, reps=3, quantum_instance=quantum_instance)
meo = MinimumEigenOptimizer(qaoa)

# This hangs for 21 stocks because the circuit/backend combination
# cannot scale to the required number of qubits in reasonable time.
result = meo.solve(qp)
print(result)
