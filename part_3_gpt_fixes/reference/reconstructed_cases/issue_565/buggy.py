import numpy as np
from qiskit import Aer
from qiskit.aqua import QuantumInstance, aqua_globals
from qiskit.quantum_info.operators import Operator, Pauli
from qiskit.aqua.operators.list_ops import SummedOp
from qiskit.aqua.algorithms import QAOA
from qiskit.aqua.components.optimizers import SPSA
from qiskit.optimization.applications.ising import tsp


def pauli(pos, num_qubits, label):
    label = 'I' * (pos) + label + 'I' * (num_qubits - pos - 1)
    assert (len(label) == num_qubits)
    return Operator(Pauli(label=label))


def s_plus(number_of_nodes, city, time):
    num_qubits = number_of_nodes ** 2
    qubit = time * number_of_nodes + city
    return pauli(qubit, num_qubits, "X") + pauli(qubit, num_qubits, "Y")


def s_minus(number_of_nodes, city, time):
    num_qubits = number_of_nodes ** 2
    qubit = time * number_of_nodes + city
    return pauli(qubit, num_qubits, "X") - pauli(qubit, num_qubits, "Y")


def create_mixer_operators(n):
    """
    Creates mixer operators for the QAOA.
    It's based on equations 54 - 58 from https://arxiv.org/pdf/1709.03489.pdf
    Indexing here comes directly from section 4.1.2 from paper 1709.03489,
    equations 54 - 58.
    """
    mixer_operators = []
    for t in range(n - 1):
        for city_1 in range(n):
            for city_2 in range(n):
                i = t
                u = city_1
                v = city_2
                first_part = 1
                first_part *= s_plus(n, u, i)
                first_part *= s_plus(n, v, i + 1)
                first_part *= s_minus(n, u, i + 1)
                first_part *= s_minus(n, v, i)
                second_part = 1
                second_part *= s_minus(n, u, i)
                second_part *= s_minus(n, v, i + 1)
                second_part *= s_plus(n, u, i + 1)
                second_part *= s_plus(n, v, i)
                mixer_operators.append(first_part + second_part)
    return mixer_operators


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

mixer = create_mixer_operators(n)
mixer_op = SummedOp(mixer)

spsa = SPSA(maxiter=300)
qaoa = QAOA(operator=qubitOp, mixer=mixer_op, p=p, optimizer=spsa, quantum_instance=quantum_instance)
circuits = qaoa.construct_circuit([0] * (2 * p))
