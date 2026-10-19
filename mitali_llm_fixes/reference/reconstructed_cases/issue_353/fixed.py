from qiskit_optimization import QuadraticProgram
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit.algorithms.minimum_eigensolvers import QAOA
from qiskit.algorithms.optimizers import COBYLA
from qiskit.primitives import Sampler
import numpy as np
import networkx as nx

n = 4
G = nx.Graph()
G.add_nodes_from(np.arange(0, n, 1))
elist = [(0, 1, 1.0), (0, 2, 1.0), (0, 3, 1.0), (1, 2, 1.0), (2, 3, 1.0)]
G.add_weighted_edges_from(elist)

n_qubits = len(G.nodes())
problem = QuadraticProgram()
_ = [problem.binary_var("x{}".format(i)) for i in range(n_qubits)]
problem.maximize(
    linear=nx.adjacency_matrix(G).dot(np.ones(n_qubits)),
    quadratic=-nx.adjacency_matrix(G),
)

meo = MinimumEigenOptimizer(QAOA(sampler=Sampler(), optimizer=COBYLA(maxiter=100)))
result = meo.solve(problem)
print(result.prettyprint())
print("\ndisplay the best 5 solution samples")
for sample in result.samples[:5]:
    print(sample)
# Print the final QAOA parameters
print(result.min_eigen_solver_result.optimal_point)
print(result.min_eigen_solver_result.optimal_parameters)
