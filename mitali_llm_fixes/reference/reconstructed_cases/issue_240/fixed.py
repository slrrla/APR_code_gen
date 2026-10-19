from qiskit.algorithms.optimizers import COBYLA

# Minimal VQE-like optimizer usage as in the qiskit VQE tutorial
def objective_function(params):
    return sum(p**2 for p in params)

num_vars = 2
initial_point = [0.1, 0.1]

optimizer = COBYLA(maxiter=1000)

# algorithms-era optimizers expose a .minimize method instead of .optimize
ret = optimizer.minimize(objective_function, x0=initial_point)
print(ret)
