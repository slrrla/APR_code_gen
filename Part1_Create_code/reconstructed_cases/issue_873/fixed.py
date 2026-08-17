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
# use SPSA.minimize(), which returns a proper SciPy-style OptimizerResult
result_obj = spsa.minimize(vqe_func, x0)
loss = result_obj.fun
x = result_obj.x
nfev = result_obj.nfev
res = OptimizeResult(
    fun=loss,
    x=x,
    nit=optimizer_config["maxiter"],
    nfev=nfev,
    message="Optimization terminated successfully.",
    success=True,
)
print(res)
