# FIX: transpile was missing -> import it, because Aer needs the custom diffuser decomposed into supported instructions
from qiskit import QuantumCircuit, QuantumRegister, Aer, transpile

def diffuser(nqubits):
    qc = QuantumCircuit(nqubits)
    for qubit in range(nqubits):
        qc.h(qubit)
    for qubit in range(nqubits):
        qc.x(qubit)
    qc.h(nqubits-1)
    qc.mct(list(range(nqubits-1)), nqubits-1)
    qc.h(nqubits-1)
    for qubit in range(nqubits):
        qc.x(qubit)
    for qubit in range(nqubits):
        qc.h(qubit)
    U_s = qc.to_gate()
    U_s.name = "U$_s$"
    return U_s

psi = QuantumRegister(3, 'psi')

backend = Aer.get_backend("statevector_simulator")
circuit = QuantumCircuit(psi)
circuit.append(diffuser(3), psi)

# FIX: Aer cannot run the custom diffuser instruction directly -> transpile the circuit for the backend, because this decomposes it into supported instructions
job = backend.run(transpile(circuit, backend))

v = job.result().get_statevector(circuit)
