import numpy, random
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Operator
from qiskit_aer import StatevectorSimulator


def define_initial_state():
    psi = numpy.zeros(16, dtype=complex)
    psi[3] = +0.5
    psi[6] = -0.5
    psi[9] = -0.5
    psi[12] = +0.5
    return psi


def define_unitary_operators():
    A1_matrix = (1 / numpy.sqrt(2)) * numpy.array([
        [1j, 0, 0, 1], [0, -1j, 1, 0], [0, 1j, 1, 0], [1, 0, 0, 1j]], dtype=complex)
    A2_matrix = (1 / 2) * numpy.array([
        [1j, 1, 1, 1j], [-1j, 1, -1, 1j], [1j, 1, -1, -1j], [-1j, 1, 1, -1j]], dtype=complex)
    A3_matrix = (1 / 2) * numpy.array([
        [-1, -1, -1, 1], [1, 1, -1, 1], [1, -1, 1, 1], [1, -1, -1, -1]], dtype=complex)
    B1_matrix = (1 / 2) * numpy.array([
        [1j, -1j, 1, 1], [-1j, -1j, 1, -1], [1, 1, -1j, 1j], [-1j, 1j, 1, 1]], dtype=complex)
    B2_matrix = (1 / 2) * numpy.array([
        [-1, 1j, 1, 1j], [1, 1j, 1, -1j], [1, -1j, 1, 1j], [-1, -1j, 1, -1j]], dtype=complex)
    B3_matrix = (1 / numpy.sqrt(2)) * numpy.array([
        [1, 0, 0, 1], [-1, 0, 0, 1], [0, 1, 1, 0], [0, 1, -1, 0]], dtype=complex)
    return {
        "A1": Operator(A1_matrix), "A2": Operator(A2_matrix), "A3": Operator(A3_matrix),
        "B1": Operator(B1_matrix), "B2": Operator(B2_matrix), "B3": Operator(B3_matrix),
    }


def create_quantum_circuit(psi, operators, x, y):
    qc = QuantumCircuit(4, 4)
    qc.initialize(psi, [0, 1, 2, 3])
    if x == 1:
        qc.unitary(operators["A1"], [2, 3], label="A1")
    elif x == 2:
        qc.unitary(operators["A2"], [2, 3], label="A2")
    elif x == 3:
        qc.unitary(operators["A3"], [2, 3], label="A3")
    if y == 1:
        qc.unitary(operators["B1"], [0, 1], label="B1")
    elif y == 2:
        qc.unitary(operators["B2"], [0, 1], label="B2")
    elif y == 3:
        qc.unitary(operators["B3"], [0, 1], label="B3")
    qc.measure([0, 1, 2, 3], [0, 1, 2, 3])
    return qc


def execute_circuit_ideal(qc, shots=2 ** 7):
    backend = StatevectorSimulator(precision="single")
    job = backend.run(transpile(qc, backend), shots=shots)
    return job.result().get_counts()


def interpret_magic_square_ideal(counts, x, y):
    wins = 0
    losses = 0
    for outcome_str, freq in counts.items():
        q3 = int(outcome_str[3])
        q2 = int(outcome_str[2])
        q1 = int(outcome_str[1])
        q0 = int(outcome_str[0])
        a3 = 0
        if q0 + q1 == 1:
            a3 = 1
        b3 = 1
        if q2 + q3 == 1:
            b3 = 0
        if y == 1:
            a = q0
        elif y == 2:
            a = q1
        elif y == 3:
            a = a3
        if x == 1:
            b = q2
        elif x == 2:
            b = q3
        elif x == 3:
            b = b3
        if a == b:
            wins += freq
        else:
            losses += freq
    return wins, losses


if __name__ == "__main__":
    random.seed(0)
    psi = define_initial_state()
    operators = define_unitary_operators()
    x = 1 + random.randrange(3)
    y = 1 + random.randrange(3)
    qc = create_quantum_circuit(psi, operators, x, y)
    counts = execute_circuit_ideal(qc)
    wins, losses = interpret_magic_square_ideal(counts, x, y)
    print(x, y, wins, losses)
