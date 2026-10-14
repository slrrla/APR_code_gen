import numpy as np
from itertools import permutations
from qiskit import Aer
from qiskit.optimization import QuadraticProgram
from qiskit.optimization.applications.ising import tsp
from qiskit.optimization.applications.ising.common import sample_most_likely
from qiskit.optimization.algorithms import MinimumEigenOptimizer
from qiskit.aqua.algorithms import QAOA


def brute_force_tsp(w):
    N = len(w)
    a = list(permutations(range(1, N)))
    best_dist = 1e10
    best_order = None
    for i in a:
        distance = 0
        pre_j = 0
        for j in i:
            distance = distance + w[pre_j, j]
            pre_j = j
        distance = distance + w[pre_j, 0]
        order = (0,) + i
        if distance < best_dist:
            best_dist = distance
            best_order = order
    return best_dist, best_order


def decodeQAOAresults(res):
    n = int(len(res) ** 0.5)
    results = np.zeros(n)
    k = 0
    for i in range(0, n):
        for j in range(0, n):
            if res[k] == 1:
                results[i] = j
            k = k + 1
    return results


def tspQuantumSolver(tspTask, backendName):
    # FIX: use the coordinates/weights pair produced together by qiskit's
    # own tsp helper instead of inventing coordinates that do not match the
    # distance matrix; this keeps w and coord consistent with each other
    isingHamiltonian, offset = tsp.get_operator(tspTask)
    tspQubo = QuadraticProgram()
    tspQubo.from_ising(isingHamiltonian, offset)

    quantumProcessor = Aer.get_backend(backendName)
    qaoa = MinimumEigenOptimizer(QAOA(quantum_instance=quantumProcessor))
    results = qaoa.solve(tspQubo)
    print('Route length: ', results.fval)
    route = decodeQAOAresults(results.x)
    print('Route: ', route)
    return results.fval, route


# FIX: generate coordinates and the corresponding distance matrix together
# with qiskit's own generator so they are guaranteed to be consistent
tspTask = tsp.random_tsp(4, seed=123)
distMatrix = tspTask.w

lengthBrute, routeBrute = brute_force_tsp(distMatrix)
print('Route length: ', lengthBrute)
print('Route: ', routeBrute)

lengthQuantum, routeQuantum = tspQuantumSolver(tspTask, 'qasm_simulator')
