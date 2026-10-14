from qiskit import QuantumCircuit, QuantumRegister, transpile

try:
    from qiskit_aer import Aer
except ImportError:
    from qiskit import Aer


def diffuser(nqubits):
    qc = QuantumCircuit(nqubits)

    # Apply transformation |s> -> |00...0>
    for qubit in range(nqubits):
        qc.h(qubit)

    # Apply transformation |00...0> -> |11...1>
    for qubit in range(nqubits):
        qc.x(qubit)

    # Apply a multi-controlled-Z gate
    qc.h(nqubits - 1)
    qc.mcx(list(range(nqubits - 1)), nqubits - 1)
    qc.h(nqubits - 1)

    # Apply transformation |11...1> -> |00...0>
    for qubit in range(nqubits):
        qc.x(qubit)

    # Apply transformation |00...0> -> |s>
    for qubit in range(nqubits):
        qc.h(qubit)

    return qc.to_gate(label="U_s")


psi = QuantumRegister(3, "psi")
circuit = QuantumCircuit(psi)
circuit.append(diffuser(3), psi)

backend = Aer.get_backend("statevector_simulator")

# Decompose the custom gate into instructions supported by the backend.
compiled_circuit = transpile(circuit, backend)

job = backend.run(compiled_circuit)
statevector = job.result().get_statevector(compiled_circuit)
del job

print(statevector)
