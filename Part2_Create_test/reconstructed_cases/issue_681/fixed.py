import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import MCXGate
from qiskit_aer.primitives import SamplerV2

def kSAT(k=3, n=3, m=3):
    qc = QuantumCircuit(n + m + 1, n + m + 1)
    qc.x(range(n, n + m))
    qc.h(range(n))

    # Problem matrix generation: {-1,0,1}^{m x n}
    matrix = np.zeros((m, n), dtype=int)
    non_zero_indices = []
    for row in range(m):
        non_zero_indices.append(np.random.choice(n, size=k, replace=False))
        matrix[row, non_zero_indices[row]] = np.random.choice([-1, 1], size=k)
    problem = matrix
    print(problem)

    # De Morgan's law
    inverse_problem = -1 * problem
    for i in range(m):
        for j in range(n):
            if inverse_problem[i][j] == -1:
                qc.x(j)
        target = non_zero_indices[i].tolist()
        mcx = MCXGate(k)
        qc.mcx(target, n + i)
        # FIX: uncompute the X gates so they don't affect later clauses.
        for j in range(n):
            if inverse_problem[i][j] == -1:
                qc.x(j)
        qc.barrier()

    qc.mcx(list(range(n, n + m)), n + m)
    return qc, problem

k = 3
n = 4
m = 20
qc, problem = kSAT(k, n, m)
qc.measure(range(n + m + 1), range(n + m + 1))

sampler = SamplerV2()
job = sampler.run([qc], shots=2048)
job_result = job.result()
counts = job_result[0].data.c.get_counts()
filtered_counts = {key: value for key, value in counts.items() if key[0] == '1'}
modified_counts = {key[-n:]: value for key, value in filtered_counts.items()}
reversed_counts = {key[-1:-n-1:-1]: value for key, value in filtered_counts.items()}
print(reversed_counts)
