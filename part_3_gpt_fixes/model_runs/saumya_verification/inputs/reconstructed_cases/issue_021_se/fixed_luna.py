import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, transpile

try:
    from qiskit_aer import Aer
except ImportError:
    from qiskit import Aer


def cnotnot(gate_label="CNOTNOT"):
    gate_circuit = QuantumCircuit(3, name=gate_label)
    gate_circuit.cx(0, 1)
    gate_circuit.cx(0, 2)

    gate = gate_circuit.to_gate()
    gate.label = gate_label
    return gate


q = QuantumRegister(3, name="q")
circuit = QuantumCircuit(q)

initial_state = [1.0 / np.sqrt(2.0), 1.0 / np.sqrt(2.0)]
circuit.initialize(initial_state, q[0])
circuit.append(cnotnot(), [q[0], q[1], q[2]])

svsim = Aer.get_backend("statevector_simulator")

# Expand the defined gate into supported primitive operations.
compiled_circuit = transpile(circuit, svsim)

result = svsim.run(compiled_circuit).result()
statevector = np.asarray(result.get_statevector(compiled_circuit))

print("a and b coefficients before simulation:", initial_state)
print("full final statevector:", statevector)

# The two nonzero branches are |000> and |111>.
final_state = [statevector[0], statevector[7]]
print("coefficients of |000> and |111>:", final_state)
