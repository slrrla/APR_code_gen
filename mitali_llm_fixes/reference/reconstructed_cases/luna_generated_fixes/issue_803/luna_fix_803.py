import numpy as np
from qiskit import QuantumCircuit, Aer, execute
from qiskit.circuit import Parameter

class QuantumCircuitWrapper:
    def __init__(self, n_qubits, backend, shots):
        self._circuit = QuantumCircuit(n_qubits)
        self.theta = Parameter('theta')
        all_qubits = list(range(n_qubits))
        self._circuit.h(all_qubits)
        self._circuit.barrier()
        self._circuit.ry(self.theta, all_qubits)
        self._circuit.measure_all()
        self.backend = backend
        self.shots = shots

    def run(self, thetas):
        circuits = [self._circuit.bind_parameters({self.theta: theta}) for theta in thetas]
        job = execute(circuits, self.backend, shots=self.shots)
        result = job.result().get_counts()
        # FIX: result is a list of count dictionaries for multiple circuits -> extract values from each dictionary, because get_counts returns one dictionary per circuit
        counts = np.array([list(circuit_counts.values()) for circuit_counts in result])
        print('counts', counts)
        # FIX: result is a list and has no values method -> get values from each count dictionary, because multiple circuits were executed
        print('result.values', [circuit_counts.values() for circuit_counts in result])
        return counts

backend = Aer.get_backend('qasm_simulator')
qc = QuantumCircuitWrapper(1, backend, 100)
thetas = [0.1, 0.2, 0.3]
print(qc.run(thetas))
