import numpy as np
from itertools import combinations
from qiskit import Aer
from qiskit.aqua import QuantumInstance, aqua_globals
from qiskit.quantum_info.operators import Pauli
from qiskit.aqua.operators import PrimitiveOp
from qiskit.aqua.operators.list_ops import SummedOp
from qiskit.aqua.algorithms import QAOA
from qiskit.aqua.components.optimizers import SPSA
from qiskit.optimization.applications.ising import tsp


def create_mixer_operators(n):
    """
    Creates mixer operators for the QAOA.
    Based on equations 54 - 58 from https://arxiv.org/pdf/1709.03489.pdf,
    but expanded by hand into a sum of simple Pauli terms so that Aqua's
    evolution machinery does not choke on composite PrimitiveOp objects
    with complex coefficients.
    """
    mixer = []
    n_qubits = pow(n, 2)
    for i in range(n - 1):
        for u, v in combinations(range(n), 2):
            qu = i * n + u
            qv = i * n + v
            x = [0] * n_qubits
            x[qu] = x[qv] = x[qu + n] = x[qv + n] = 1
            Hi = 0
            # XXXX term
            z = [0] * n_qubits
            term = Pauli(z, x)
            term = PrimitiveOp(term)
            Hi += term
            # YYYY term
            z = [0] * n_qubits
            z[qu] = z[qv] = z[qu + n] = z[qv + n] = 1
            term = Pauli(z, x)
            term = PrimitiveOp(term)
            Hi += term
            # terms with two Ys (XXYY and similar)
            for q0, q1 in combinations([qu, qv, qu + n, qv + n], 2):
                z = [0] * n_qubits
                z[q0] = z[q1] = 1
                term = Pauli(z, x)
                coeff = 1
                if (q0, q1) in [(qu, qv), (qu + n, qv + n)]:
                    coeff = -1
                term = PrimitiveOp(term, coeff)
                Hi += term
            mixer.append(2 * Hi)
    return SummedOp(mixer)


seed = 10598
n = 3
p = 2
num_qubits = n ** 2

# Generate random tsp
ins = tsp.random_tsp(n, seed=seed)
qubitOp, offset = tsp.get_operator(ins)

# Running in quantum simulation
aqua_globals.random_seed = np.random.default_rng(seed)
backend = Aer.get_backend('qasm_simulator')
quantum_instance = QuantumInstance(backend, seed_simulator=seed, seed_transpiler=seed)

mixer_op = create_mixer_operators(n)

spsa = SPSA(maxiter=300)
qaoa = QAOA(operator=qubitOp, mixer=mixer_op, p=p, optimizer=spsa, quantum_instance=quantum_instance)
circuits = qaoa.construct_circuit([0] * (2 * p))
