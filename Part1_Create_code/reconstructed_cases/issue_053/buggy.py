import numpy as np
import torch
from qiskit import QuantumCircuit as QK_QuantumCircuit, Aer, execute
from qiskit.circuit import Parameter

class QuantumCircuit:
    """ Minimal quantum circuit wrapper, as used in the qiskit textbook tutorial """
    def __init__(self, n_qubits, backend, shots):
        self._circuit = QK_QuantumCircuit(n_qubits)
        all_qubits = list(range(n_qubits))
        self.theta = Parameter('theta')
        self._circuit.h(all_qubits)
        self._circuit.barrier()
        self._circuit.ry(self.theta, all_qubits)
        self._circuit.measure_all()
        self.backend = backend
        self.shots = shots
        self.shift = 0.01

    def run(self, thetas):
        # placeholder expectation value computation
        return np.array([np.cos(t) for t in thetas]).mean()

class HybridFunction(torch.autograd.Function):
    """ Hybrid quantum - classical function definition """

    @staticmethod
    def forward(ctx, input, quantum_circuit, shift):
        ctx.shift = shift
        ctx.quantum_circuit = quantum_circuit
        expectation_z = ctx.quantum_circuit.run(input.tolist())
        result = torch.tensor([expectation_z])
        ctx.save_for_backward(input, result)
        return result

    @staticmethod
    def backward(ctx, grad_output):
        """ Backward pass computation """
        input, expectation_z = ctx.saved_tensors
        input_list = np.array(input.tolist())

        shift_right = input_list + np.ones(input_list.shape) * ctx.shift
        shift_left = input_list - np.ones(input_list.shape) * ctx.shift

        gradients = []
        for i in range(len(input_list)):
            expectation_right = ctx.quantum_circuit.run(shift_right[i])
            expectation_left  = ctx.quantum_circuit.run(shift_left[i])

            gradient = torch.tensor([expectation_right]) - torch.tensor([expectation_left])
            gradients.append(gradient)
        gradients = np.array([gradients]).T
        return torch.tensor([gradients]).float() * grad_output.float(), None, None

# Example usage
qc = QuantumCircuit(1, Aer.get_backend('qasm_simulator'), 100)
inp = torch.tensor([0.5], requires_grad=True)
out = HybridFunction.apply(inp, qc, 0.01)
out.backward(torch.tensor([1.0]))
