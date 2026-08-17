from qiskit import QuantumCircuit, QuantumRegister


def plus_one(qubit_number: int):
    # Use ancilla qubits to store intermediate "prefix AND" results so that
    # each flip only needs a 2-qubit controlled gate (CCX) instead of an
    # ever-growing MCX gate. This avoids the expensive multi-controlled
    # gates that made transpilation slow in the original implementation.
    data = QuantumRegister(qubit_number, name="q")
    anc = QuantumRegister(max(qubit_number - 1, 1), name="anc")
    circuit = QuantumCircuit(data, anc, name="plus_one")

    if qubit_number > 1:
        # compute prefix ANDs of the data qubits into the ancillas
        circuit.cx(data[0], anc[0])
        for i in range(1, qubit_number - 1):
            circuit.ccx(anc[i - 1], data[i], anc[i])

        # flip bits from most significant to least significant, controlled
        # by the appropriate prefix-AND ancilla
        circuit.cx(anc[qubit_number - 2], data[qubit_number - 1])
        for i in range(qubit_number - 2, 0, -1):
            circuit.cx(anc[i - 1], data[i])

    circuit.x(data[0])

    if qubit_number > 1:
        # uncompute the ancillas so they are returned to the |0> state
        for i in range(qubit_number - 2, 0, -1):
            circuit.ccx(anc[i - 1], data[i], anc[i])
        circuit.cx(data[0], anc[0])

    return circuit.to_gate()


# Example usage: only 2-qubit controlled gates are used now, so
# transpilation stays fast even for larger qubit_number values.
qc = QuantumCircuit(4)
qc.append(plus_one(4), range(4))
print(qc.decompose())
