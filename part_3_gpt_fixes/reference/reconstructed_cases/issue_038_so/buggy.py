import networkx as nx
from qiskit import Aer
from qiskit.algorithms import QAOA, NumPyMinimumEigensolver
from qiskit.algorithms.optimizers import COBYLA
from qiskit_optimization import QuadraticProgram
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_optimization.applications import Maxcut
from qiskit.utils import QuantumInstance

# Define the edges of the graph (edges are represented by tuples of node indices)
edges = [(0, 1), (0, 2), (1, 2)]

# Create a graph based on these edges
G = nx.Graph(edges)

# Create the Maxcut object
maxcut = Maxcut(G)

# Create a QuadraticProgram based on maxcut
qp = maxcut.to_quadratic_program()

# Solve the problem exactly using classical eigensolver
exact_mes = NumPyMinimumEigensolver()
exact = MinimumEigenOptimizer(exact_mes)
result = exact.solve(qp)
print("Exact solution:\n", result)

# Solve the problem using QAOA
quantum_instance = QuantumInstance(Aer.get_backend('statevector_simulator'))
qaoa_mes = QAOA(optimizer=COBYLA(), quantum_instance=quantum_instance)
qaoa = MinimumEigenOptimizer(qaoa_mes)
result = qaoa.solve(qp)
print("QAOA solution:\n", result)
