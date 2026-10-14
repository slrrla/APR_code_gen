import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, BasicAer, IBMQ
from qiskit import Aer
from qiskit.visualization import plot_histogram, plot_bloch_multivector
from qiskit import *
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram
from qiskit.extensions import Initialize
from qiskit.quantum_info import Statevector, random_statevector

# random statevector generated from |0> state.
def random_state(nqubits):
    """Creates a random nqubit state vector"""
    from numpy import append, array, sqrt
    from numpy.random import random
    real_parts = array([])
    im_parts = array([])
    for amplitude in range(2**nqubits):
        real_parts = append(real_parts, (random()*2)-1)
        im_parts = append(im_parts, (random()*2)-1)
    # Combine into list of complex numbers:
    amps = real_parts + 1j*im_parts
    # Normalise
    magnitude_squared = 0
    for a in amps:
        magnitude_squared += abs(a)**2
    amps /= sqrt(magnitude_squared)
    return amps

psi = random_state(1)
# Initialize the state to be teleported
init_gate = Initialize(psi)

# quantum circuit for getting statevector from initialize objects.
qc_init = QuantumCircuit(1, global_phase=0)
# Check initial random state
print("initial random state")
print(init_gate)
qc_init.append(init_gate, [0])
print(qc_init)
compiled_circuit_init = transpile(qc_init, Aer.get_backend('statevector_simulator'))
simulator_init = Aer.get_backend('statevector_simulator')
result_init = simulator_init.run(compiled_circuit_init).result()
init_statevector = result_init.get_statevector()

# use evolve to change Initialize method to Statevector.
statevector_bell = Statevector.from_label('00')
# Combine the individual statevectors using tensor product
compound_statevector = init_statevector.tensor(statevector_bell)
print("tensor product result\n")
print(compound_statevector.data)

# qc is stage1. generate Bell state and operate in Alice's side
qc = QuantumCircuit(3, 2, global_phase=0)
# Prepare an entangled Bell pair between Alice and Bob
qc.h(1)
qc.cx(1, 2)
qc.barrier()
# Entangle the state to be teleported with Alice's qubit
qc.cx(0, 1)
qc.h(0)
# evolve compound statevector through evolve method.
compound_statevector = compound_statevector.evolve(qc)
print(qc)
print("result\n")
print(compound_statevector.data)

# qc1 is stage2. measure Alice's side
qc1 = QuantumCircuit(3, 2, global_phase=0)
# Measurement on Alice's qubits
qc1.initialize(compound_statevector, [0, 1, 2])
qc1.measure([0, 1], [0, 1])
# Print the circuit and execute to obtain Alice's measurement result
print("Measurement outcomes for Alice's qubits:")
print(qc1)
simulator = BasicAer.get_backend('statevector_simulator')
job_alice = execute(qc1, simulator, shots=1)
result_alice = job_alice.result()
statevector_alice = result_alice.get_statevector()
print(statevector_alice)
alice_measurement_result = list(result_alice.get_counts(qc1).keys())[0]
# Display Alice's measurement result and wait for user input
print("Alice's measured information:", alice_measurement_result)
input("Press Enter to continue and apply corrections to Bob's qubit")

# qc2 is stage3. Bob implement operation.
qc2 = QuantumCircuit(3, 1, global_phase=0)
# typing measured output and feed into bob's quantum circuit will be implemented.
qc2.initialize(statevector_alice, [0, 1, 2])
# Apply corrections to Bob's qubit based on Alice's measurement result
if alice_measurement_result[0] == '1':
    qc2.z(2)
if alice_measurement_result[1] == '1':
    qc2.x(2)
print("Complete Quantum Circuit:")
print(qc2)
job_bob = execute(qc2, simulator, shots=1)
result_bob = job_bob.result()
statevector_bob = result_bob.get_statevector()
print("Measurement outcomes for Bob's qubit:")
print(statevector_bob)
