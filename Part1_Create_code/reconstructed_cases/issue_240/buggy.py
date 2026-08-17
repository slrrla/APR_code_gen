from qiskit.aqua.components.optimizers import COBYLA

# Minimal VQE-like optimizer usage as in the qiskit VQE tutorial
def objective_function(params):
    return sum(p**2 for p in params)

num_vars = 2
initial_point = [0.1, 0.1]

optimizer = COBYLA(maxiter=1000)

# aqua-era optimizers exposed an .optimize method
ret = optimizer.optimize(num_vars, objective_function, initial_point=initial_point)
print(ret)
