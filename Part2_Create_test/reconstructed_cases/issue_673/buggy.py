import numpy as np
import matplotlib.pyplot as plt
import random
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute
import qiskit
from qiskit_aer import AerSimulator

def create_registers():
    alice_q = QuantumRegister(1, 'alice (q)')
    peter_alice_q = QuantumRegister(1, 'peter/alice (q)')
    peter_bob_q = QuantumRegister(1, 'peter/bob (q)')
    bob_c = ClassicalRegister(3, 'bob (c)')
    circ = QuantumCircuit(alice_q, peter_alice_q, peter_bob_q, bob_c)
    return circ

circ = create_registers()
circ.x(2).c_if(1, 1)
circ.measure(2, 2)

device = AerSimulator()
shots = 1000

# basis_gates is missing required gates ('measure', etc.) causing a
# TranspilerError: Unable to translate the operations in the circuit
circ = qiskit.compiler.transpile(circ, basis_gates=['x', 'if_else'])
job = execute(circ, backend=device, shots=shots)
