import networkx as nx
from qiskit.optimization.applications.ising import stable_set

# The user attempts to convert a QUBO matrix directly using stable_set.get_operator,
# but this function expects a graph adjacency matrix, not a general QUBO matrix.
path = nx.to_numpy_array(nx.path_graph(3))
qubitOp, offset = stable_set.get_operator(path)
print('Offset:', offset)
print('Ising Hamiltonian:')
print(qubitOp.print_details())
