from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import HRSCumulativeMultiplier
from qiskit_aer import AerSimulator
from qiskit import transpile

n_bit = 8

# Define quantum registers
first_operand = QuantumRegister(n_bit, 'operand_a')
second_operand = QuantumRegister(n_bit, 'operand_b')
multiplication_result = QuantumRegister(n_bit, 'result')
aux = QuantumRegister(1, 'aux')

qc = QuantumCircuit(first_operand, second_operand, multiplication_result, aux)

# All Superposition
qc.h(first_operand)
qc.h(second_operand)

expected_result = '10110100'  # 180 in decimal
print(f'Expected: {expected_result}')

# Multiplier
multiplier = HRSCumulativeMultiplier(num_state_qubits=n_bit, num_result_qubits=n_bit)
qc.append(multiplier, qargs=list(first_operand) + list(second_operand) + list(multiplication_result) + list(aux))
qc.barrier()

for i, v in enumerate(expected_result[::-1]):
    if v == '0':
        qc.x(multiplication_result[i])
qc.barrier()
qc.h(multiplication_result[-1])
qc.mcx(multiplication_result[:-1], multiplication_result[-1])
qc.h(multiplication_result[-1])
qc.barrier()
for i, v in enumerate(expected_result[::-1]):
    if v == '0':
        qc.x(multiplication_result[i])
qc.barrier()

# Diffuser
# BUG: diffuser is applied over ALL registers (including result and aux),
# and the multiplier is never uncomputed before the diffuser is applied.
qc.h(first_operand)
qc.h(second_operand)
qc.h(multiplication_result)
qc.h(aux)
qc.x(first_operand)
qc.x(second_operand)
qc.x(multiplication_result)
qc.x(aux)
qc.barrier()
qc.h(aux)
qc.mcx(list(range(n_bit * 3)), aux)
qc.h(aux)
qc.barrier()
qc.x(first_operand)
qc.x(second_operand)
qc.x(multiplication_result)
qc.x(aux)
qc.h(first_operand)
qc.h(second_operand)
qc.h(multiplication_result)
qc.h(aux)

qc.measure_all()

sim = AerSimulator()
qc_t = transpile(qc, sim)
counts = sim.run(qc_t, shots=1024).result().get_counts()
print(counts)
