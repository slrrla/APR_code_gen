from qiskit import QuantumCircuit, assemble
from qiskit import Aer
import numpy as np

np.random.seed(222)


def one_shot(operator):
    sim = Aer.get_backend("aer_simulator")
    qc = QuantumCircuit(2)
    unitary = [[qc.h], [qc.sdg, qc.h], [qc.id]]
    qc.h(0)
    qc.cx(0, 1)
    for gate in unitary[operator[0]]:
        gate(0)
    for gate in unitary[operator[1]]:
        gate(1)
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
states = [state0, state1]
record_rho = np.zeros([4, 4])

for i in range(snapshot_num):
    randnum = np.random.randint(0, 3, size=2)
    result = one_shot(randnum)
    bit0, bit1 = [int(x) for x in list(result.keys())[0]]
    U0, U1 = unitary[randnum[0]], unitary[randnum[1]]
    rhohat = np.kron(3 * U0.conj().T @ states[bit0] @ U0 - id, 3 * U1.conj().T @ states[bit1] @ U1 - id)
    record_rho = record_rho + rhohat

record_rho = record_rho / snapshot_num
bell_state = np.array([[0.5, 0, 0, 0.5], [0, 0, 0, 0], [0, 0, 0, 0], [0.5, 0, 0, 0.5]])
print("State distance")
print(distance(record_rho - bell_state))
