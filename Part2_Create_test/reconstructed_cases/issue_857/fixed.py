from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, Aer, execute
from qiskit.providers.aer.noise import NoiseModel, errors
# importing this module registers save_statevector (and friends) as
# methods on QuantumCircuit -- required for older Aer/Terra versions
from qiskit.providers.aer.library import save_statevector

class Simulation:
    def __init__(self, error_rates):
        self.error_rates = error_rates
        # c/q register
        self.qubits = QuantumRegister(9)
        self.round1 = ClassicalRegister(2)
        self.round2 = ClassicalRegister(3)
        self.decoded = ClassicalRegister(7)
        self.circuit = QuantumCircuit(self.qubits, self.round1, self.round2, self.decoded, name="circuit")
        # noise model
        self.noisy = NoiseModel()
        self.error_rate = self.error_rates
        self.error_two_qubit = errors.depolarizing_error(self.error_rate / 15, 2)
        self.noisy.add_all_qubit_quantum_error(self.error_two_qubit, ['cx', 'cz', 'cy'])
        # simulator backend
        self.simulator = Aer.get_backend('qasm_simulator')

    def stabilizer_round(self, target1, target2, target3, target4):
        self.circuit.reset(self.qubits[7])
        self.circuit.reset(self.qubits[8])
        self.circuit.h(self.qubits[8])
        self.circuit.cx(self.qubits[8], self.qubits[7])
        self.circuit.cx(self.qubits[target1], self.qubits[7])
        self.circuit.cx(self.qubits[target2], self.qubits[8])
        self.circuit.cx(self.qubits[target3], self.qubits[7])
        self.circuit.cx(self.qubits[target4], self.qubits[8])
        self.circuit.cx(self.qubits[8], self.qubits[7])
        self.circuit.h(self.qubits[8])
        self.circuit.measure(self.qubits[7], self.round1[0])
        self.circuit.measure(self.qubits[8], self.round1[1])
        self.circuit.save_statevector()

    def run(self):
        self.result = execute(self.circuit, self.simulator, shots=1).result()
        self.statevector = self.result.get_statevector(self.circuit)


sim = Simulation(0.01)
sim.stabilizer_round(0, 1, 2, 3)
sim.run()
