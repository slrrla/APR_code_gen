from qiskit import QuantumCircuit

circ = QuantumCircuit(2, 2)
circ.x(1)
circ.h(0)
circ.h(1)
circ.cx(0, 1)
circ.h(0)
circ.measure(0, 0)
circ.measure(1, 1)

# Naive attempt: just walk the instruction list and assume each
# instruction is its own "layer" -- this does NOT group gates that
# act in parallel (e.g. the initial X on q1 and H on q0), so it does
# not actually decompose the circuit into layers.
for i, instruction in enumerate(circ.data):
    print(f"layer[{i}] = [{instruction.operation.name} {instruction.qubits}]")
