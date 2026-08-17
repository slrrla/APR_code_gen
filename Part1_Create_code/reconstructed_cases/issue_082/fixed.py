import numpy as np
import time
from qiskit import QuantumCircuit
from qiskit.quantum_info import random_unitary
from qiskit_aer import AerSimulator
from qiskit.compiler import transpile
import opt_einsum as oe


class Gate:
    def __init__(self, qubits, unitary, name=None):
        self.qubits = qubits  # span of qubits on which the gate acts
        self.unitary = unitary  # unitary matrix representing the gate
        self.name = name

    def __repr__(self):
        return f'Gate(qubits={self.qubits}, unitary=\n{self.unitary})'


def get_gate_list(qc):
    gates_list = []
    n_qubits = qc.num_qubits
    for instruction in qc.data:
        gate_operation = instruction.operation
        qubits = [qubit._index for qubit in instruction.qubits]
        gates_list.append(Gate(qubits, gate_operation.to_matrix(), gate_operation.name))
    return gates_list


def get_unitary_with_qiskit(qc):
    simulator = AerSimulator(method='unitary', device='CPU')
    qc.save_unitary()
    transpiled_circuit = transpile(qc, simulator)
    start_time = time.time()
    job = simulator.run(transpiled_circuit)
    result = job.result()
    unitary_matrix = result.get_unitary(transpiled_circuit)
    end_time = time.time()
    execution_time_ms = (end_time - start_time) * 1000
    return unitary_matrix, execution_time_ms


def create_random_unitary(num_qubits_chosen, seed):
    return random_unitary(2 ** num_qubits_chosen, seed=seed)


def single_contraction_test():
    num_qubits = 2
    # create a circuit with a gate spanning both qubits and one spanning the first qubit
    circuit = QuantumCircuit(num_qubits)
    seed = 42
    np.random.seed(seed)
    circuit.unitary(create_random_unitary(num_qubits, seed), range(num_qubits))
    circuit.unitary(create_random_unitary(num_qubits - 1, seed), range(num_qubits - 1))
    return circuit


def get_error(matrix1, matrix2):
    """Calculate the Frobenius norm of the difference between two matrices."""
    diff = matrix1 - matrix2
    error = np.sqrt(np.sum(np.abs(diff) ** 2))
    return error


def contract_opteinsum(qc):
    gate_list = get_gate_list(qc)
    # Get the gates in reverse order (since we apply right to left)
    A_gate = gate_list[0]  # Two-qubit gate (applies second)
    B_gate = gate_list[1]  # Single-qubit gate (applies first)
    A_qubits = A_gate.qubits[::-1]
    B_qubits = B_gate.qubits[::-1]
    U_A = A_gate.unitary.reshape([2] * 2 * qc.num_qubits)
    U_B = B_gate.unitary.reshape([2] * 2 * (qc.num_qubits - 1))
    all_letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    A_index = all_letters[:2 * len(A_gate.qubits)]
    qubits_in_common = set(A_gate.qubits) & set(B_gate.qubits)
    B_index = all_letters[2 * len(A_gate.qubits):2 * len(A_gate.qubits) + 2 * len(B_gate.qubits)]
    for qubit in qubits_in_common:
        B_index = B_index.replace(B_index[len(B_qubits) + B_qubits.index(qubit)], A_index[A_qubits.index(qubit)])
    C_index = A_index[:]
    for qubit in qubits_in_common:
        C_index = C_index.replace(C_index[A_qubits.index(qubit)], B_index[B_qubits.index(qubit)])
    einsum_str = f'{A_index},{B_index}->{C_index}'
    print(einsum_str)
    start_time = time.time()
    result_matrix = np.einsum(einsum_str, U_A, U_B)
    end_time = time.time()
    result_matrix = result_matrix.reshape(2 ** qc.num_qubits, 2 ** qc.num_qubits)
    return result_matrix, (end_time - start_time) * 1000


def main():
    qc = single_contraction_test()
    unitary_matrix_oe, execution_time_ms_oe = contract_opteinsum(qc)
    unitary_matrix, execution_time_ms = get_unitary_with_qiskit(qc)
    print(f'Qiskit execution time: {execution_time_ms} ms')
    print(f'Opteinsum execution time: {execution_time_ms_oe} ms')
    print(f'Error between Qiskit and Opteinsum: {get_error(unitary_matrix, unitary_matrix_oe)}')


if __name__ == '__main__':
    main()
