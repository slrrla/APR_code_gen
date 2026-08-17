from qiskit import transpile
from qiskit.circuit.library import QuantumVolume

# Build a circuit and transpile it to u3/cx basis
qc = QuantumVolume(2)
tqc = transpile(qc, optimization_level=3, basis_gates=["u3", "cx"], seed_transpiler=1)

# Programmatically extract every U3 gate's qubit and parameters
gate_val = 0
u3_dir = {}
for i, instruction in enumerate(tqc.data):
    if instruction.operation.name == 'u3':
        u3_dir['u3_' + str(gate_val)] = {
            'qubit': instruction.qubits[0],
            'params': instruction.operation.params
        }
        gate_val += 1

print(u3_dir)
