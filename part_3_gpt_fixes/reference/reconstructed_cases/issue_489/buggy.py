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


def tspQuantumSolver(distances, backendName):
    citiesNumber = len(distances)
    # BUG: coordinates do not correspond to the given distance matrix at all,
    # they are simply placed along a straight line (i+1, 0) regardless of
    # the real distances between the cities
    coordinates = np.zeros([citiesNumber, 2])
    for i in range(0, citiesNumber):
        coordinates[i][0] = i + 1

    tspTask = tsp.TspData(name='TSP', dim=citiesNumber, w=distances, coord=coordinates)
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


distMatrix = np.array([[0, 207, 92, 131],
                        [207, 0, 300, 350],
                        [92, 300, 0, 82],
                        [131, 350, 82, 0]])

lengthBrute, routeBrute = brute_force_tsp(distMatrix)
print('Route length: ', lengthBrute)
print('Route: ', routeBrute)

lengthQuantum, routeQuantum = tspQuantumSolver(distMatrix, 'qasm_simulator')
