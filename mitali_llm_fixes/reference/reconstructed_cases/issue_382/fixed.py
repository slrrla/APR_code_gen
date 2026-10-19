from qiskit import QuantumCircuit


def cf(circuit, qubit1, qubit2):
    # Create a circuit that is equivalent to your gate:
    qc = QuantumCircuit(2)
    qc.cx(0, 1)
    qc.csx(1, 0)
    qc.cx(0, 1)
    # Convert the circuit to a gate:
    sr_swap = qc.to_gate(label='√SWAP')
    # Add the gate to your circuit which is passed as the first argument to cf function:
    circuit.append(sr_swap, [qubit1, qubit2])


# We need this line to add the method to QuantumCircuit class:
QuantumCircuit.cf = cf

circ = QuantumCircuit(2, 2)
circ.h(0)
circ.cf(0, 1)
circ.draw('mpl')
