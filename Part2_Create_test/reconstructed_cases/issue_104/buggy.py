from qiskit import QuantumCircuit

def plus_one(qubit_number: int):
    circuit = QuantumCircuit(qubit_number, name="plus_one")
    # iterate from most significant to least significant qubit
    # if all less significant qubits are 1, flip the current qubit
    for q in reversed(range(1, qubit_number)):
        circuit.mcx([x for x in range(0, q)], q, ctrl_state=(2**q) - 1)
    circuit.x(0)
    return circuit.to_gate()


# Example usage: this works but transpilation becomes very slow
# for larger qubit_number because of the growing MCX gates.
qc = QuantumCircuit(4)
qc.append(plus_one(4), range(4))
print(qc.decompose())
