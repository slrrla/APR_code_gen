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
        # get_counts() returns a list of dicts because we submitted multiple circuits
        counts_list = job.result().get_counts()
        for _dict in counts_list:
            print(_dict)
        return counts_list

backend = Aer.get_backend('qasm_simulator')
qc = QuantumCircuitWrapper(1, backend, 100)
thetas = [0.1, 0.2, 0.3]
print(qc.run(thetas))
