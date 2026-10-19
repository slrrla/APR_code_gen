import numpy as np
from qiskit.algorithms.optimizers import SPSA
from scipy.optimize import OptimizeResult


def vqe_func(params):
    # placeholder objective function standing in for the VQE energy evaluation
    return np.sum(np.square(params))


num_params = 3
x0 = np.random.rand(num_params)
optimizer_config = {"maxiter": 100}


def callback(*args):
    pass


spsa = SPSA(**optimizer_config, callback=callback)
# deprecated: SPSA.optimize() returns a plain tuple, not a SciPy OptimizerResult
x, loss, nfev = spsa.optimize(num_params, vqe_func, initial_point=x0)
res = OptimizeResult(
    fun=loss,
    x=x,
    nit=optimizer_config["maxiter"],
    nfev=nfev,
    message="Optimization terminated successfully.",
    success=True,
)
print(res)
