from qiskit import QuantumCircuit, assemble
from qiskit import Aer
import numpy as np

np.random.seed(222)


def one_shot(operator):
    sim = Aer.get_backend("aer_simulator")
    qc = QuantumCircuit(2)
    unitary = [qc.h, qc.sdg, qc.id]
    qc.h(0)
    qc.cx(0, 1)
    unitary[operator[0]](0)
    unitary[operator[1]](1)
    qc.measure_all()
    qobj = assemble(qc, shots=1)
    result = sim.run(qobj).result().get_counts()
    return result


def distance(rho):
    return np.sqrt(np.trace(rho.conjugate().transpose().dot(rho)))


hadamard = 1 / np.sqrt(2) * np.array([[1, 1], [1, -1]])
s_gate = np.array([[1, 0], [0, -1j]], dtype=complex)
id = np.identity(2)
unitary = [hadamard, np.dot(hadamard, s_gate), id]

snapshot_num = 300
state0 = np.array([[1, 0], [0, 0]])
state1 = np.array([[0, 0], [0, 1]])
record_rho = np.zeros([4, 4])

for i in range(snapshot_num):
    randnum = np.random.randint(0, 3, size=2)
    result = one_shot(randnum)
    if result.get("00") == 1:
        rho = np.kron(3 * np.dot(unitary[randnum[0]].conj().T, state0).dot(unitary[randnum[0]] - id), 3 * np.dot(unitary[randnum[1]].conj().T, state0).dot(unitary[randnum[1]]) - id)
    elif result.get("01") == 1:
        rho = np.kron(3 * np.dot(unitary[randnum[0]].conj().T, state0).dot(unitary[randnum[0]] - id), 3 * np.dot(unitary[randnum[1]].conj().T, state1).dot(unitary[randnum[1]]) - id)
    elif result.get("10") == 1:
        rho = np.kron(3 * np.dot(unitary[randnum[0]].conj().T, state1).dot(unitary[randnum[0]] - id), 3 * np.dot(unitary[randnum[1]].conj().T, state0).dot(unitary[randnum[1]]) - id)
    else:
        rho = np.kron(3 * np.dot(unitary[randnum[0]].conj().T, state1).dot(unitary[randnum[0]] - id), 3 * np.dot(unitary[randnum[1]].conj().T, state1).dot(unitary[randnum[1]]) - id)
    record_rho = record_rho + rho

record_rho = record_rho / snapshot_num
bell_state = np.array([[0.5, 0, 0, 0.5], [0, 0, 0, 0], [0, 0, 0, 0], [0.5, 0, 0, 0.5]])
print("State distance")
print(distance(record_rho - bell_state))
