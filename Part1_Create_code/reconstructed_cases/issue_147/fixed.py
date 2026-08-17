from qiskit import Aer
from qiskit.optimization import QuadraticProgram
from qiskit.aqua.algorithms import QAOA
from qiskit.optimization.algorithms import MinimumEigenOptimizer

# construct optimization problem
qp = QuadraticProgram()
qp.binary_var('x1')
qp.binary_var('x2')
qp.minimize(linear=[5, -7])

# initialize optimizer
qaoa_mes = QAOA(quantum_instance=Aer.get_backend('statevector_simulator'))
qaoa = MinimumEigenOptimizer(qaoa_mes)

# solve problem
result = qaoa.solve(qp)
print(result)
