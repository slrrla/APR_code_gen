# imports
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.circuit.library import HRSCumulativeMultiplier
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator

sim = AerSimulator()

expected_result = '10101'  # 21 in decimal
n_bit = len(expected_result)  # number of qubits
print(f'Expected: {expected_result}')


# function to mark element
def mark_elem(expected_result):
    n = len(expected_result)
    qc = QuantumCircuit(n, name=' Mark Elem')
    for i, v in enumerate(expected_result[::-1]):
        if v == '0':
            qc.x(i)
    qc.barrier()
    qc.h(n - 1)
    qc.mcx(list(range(n - 1)), n - 1)
    qc.h(n - 1)
    qc.barrier()
    for i, v in enumerate(expected_result[::-1]):
        if v == '0':
            qc.x(i)
    return qc


# function for diffuser
def diffuser(n):
    qc = QuantumCircuit(n, name=' Diffuser')
    qc.h(range(n))
    qc.x(range(n))
    qc.barrier()
    qc.h(n - 1)
    qc.mcx(list(range(n - 1)), n - 1)
    qc.h(n - 1)
    qc.barrier()
    qc.x(range(n))
    qc.h(range(n))
    return qc


# multiplier gate
multiplier = HRSCumulativeMultiplier(num_state_qubits=n_bit, num_result_qubits=n_bit)

# Define quantum registers
first_operand = QuantumRegister(n_bit, 'operand_a')
second_operand = QuantumRegister(n_bit, 'operand_b')
multiplication_result = QuantumRegister(n_bit, 'result')
aux = QuantumRegister(1, 'aux')
first_meas = ClassicalRegister(n_bit, 'a_m')
second_meas = ClassicalRegister(n_bit, 'b_m')

qc = QuantumCircuit(first_operand, second_operand, multiplication_result, aux, first_meas, second_meas)

# initialize operands in superposition
qc.h(first_operand)
qc.h(second_operand)

# iterate to apply oracle+diffuser
for i in range(6):
    qc.append(multiplier, qargs=list(first_operand) + list(second_operand) + list(multiplication_result) + list(aux))
    qc.append(mark_elem(expected_result), multiplication_result)
    qc.append(multiplier.inverse(), qargs=list(first_operand) + list(second_operand) + list(multiplication_result) + list(aux))
    qc.append(diffuser(2 * n_bit), range(2 * n_bit))
    qc.barrier()

qc.measure(first_operand, first_meas)
qc.measure(second_operand, second_meas)

# transpile, run sim, extract results
qc_t = transpile(qc, sim)
counts = sim.run(qc_t, shots=2 ** 14).result().get_counts()
counts_new = {str(int(key[0:n_bit + 1], 2)) + ' ' + str(int(key[n_bit + 1:], 2)): value for key, value in counts.items()}
plot_histogram(counts_new, figsize=(30, 5))
