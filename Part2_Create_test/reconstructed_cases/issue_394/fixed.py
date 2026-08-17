from qiskit import QuantumCircuit, execute
from qiskit.circuit.library import RGQFTMultiplier
from qiskit_aer import AerSimulator

num_bits = 28  # bit-width that starts showing wrong results

input1 = 0xc452632
input2 = 0x8fac911

qc = QuantumCircuit(4 * num_bits)

# load input1 and input2 into the first two registers of num_bits qubits each
for i in range(num_bits):
    if (input1 >> i) & 1:
        qc.x(i)
    if (input2 >> i) & 1:
        qc.x(num_bits + i)

multiplier = RGQFTMultiplier(num_state_qubits=num_bits)
qc.append(multiplier.to_instruction(), range(4 * num_bits))
qc.measure_all()

# increase the bond dimension of the MPS simulator to get exact results
# (exponentially more expensive in memory/time, but avoids truncation error)
backend = AerSimulator(
    method='matrix_product_state',
    matrix_product_state_max_bond_dimension=100000,
    matrix_product_state_truncation_threshold=1e-16,
)

result = execute(qc, backend, shots=1024).result()
counts = result.get_counts()
print(counts)
