import networkx as nx
from qiskit import QuantumCircuit, Aer, execute
from scipy.optimize import minimize

# Simple graph for MaxCut/QAOA
G = nx.Graph()
G.add_edges_from([(0, 1), (1, 2), (2, 0)])


def maxcut_obj(bitstring, G):
    x = [int(b) for b in bitstring]
    obj = 0
    for i, j in G.edges():
        if x[i] != x[j]:
            obj -= 1
    return obj


def compute_expectation(counts, G):
    avg = 0
    sum_count = 0
    for bitstring, count in counts.items():
        obj = maxcut_obj(bitstring, G)
        avg += obj * count
        sum_count += count
    return avg / sum_count


def create_qaoa_circ(G, theta):
    nqubits = len(G.nodes())
    p = len(theta) // 2
    qc = QuantumCircuit(nqubits)
    beta = theta[:p]
    gamma = theta[p:]

    for i in range(nqubits):
        qc.h(i)

    for irep in range(p):
        for pair in list(G.edges()):
            qc.rzz(2 * gamma[irep], pair[0], pair[1])
        for i in range(nqubits):
            qc.rx(2 * beta[irep], i)

    qc.measure_all()
    return qc


def get_expectation(G, p=1, shots=512):
    backend = Aer.get_backend('qasm_simulator')
    backend.shots = shots

    def execute_circ(theta):
        qc = create_qaoa_circ(G, theta)
        counts = execute(qc, backend, seed_simulator=10, shots=shots).result().get_counts()
        return compute_expectation(counts, G)

    return execute_circ


expectation = get_expectation(G, p=1)
# Using scipy's minimize with a Qiskit optimizer name -> fails
res = minimize(expectation, [1.0, 1.0], method='ADAM')
print(res)
