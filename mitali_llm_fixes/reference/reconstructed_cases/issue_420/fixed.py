from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Pauli
from qiskit.synthesis import SuzukiTrotter
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.providers.fake_provider import FakeJakarta

hamiltonian = Pauli('XYZIZYX')

# Use a local fake backend with limited qubit connectivity instead of
# contacting a real IBM Quantum device.
backend = FakeJakarta()

for cx_structure in ['chain', 'fountain']:
    evo_time = 1.0
    # Suzuki-Trotter product formula of order 2 and one time step:
    synthesis = SuzukiTrotter(order=2, reps=1, cx_structure=cx_structure)
    gate = PauliEvolutionGate(hamiltonian, evo_time, synthesis=synthesis)
    circ = QuantumCircuit(hamiltonian.num_qubits)
    circ.append(gate, range(hamiltonian.num_qubits))
    trns_circ = transpile(
        circ, backend=backend, layout_method='sabre', routing_method='sabre'
    )
    print(cx_structure, trns_circ.depth())
