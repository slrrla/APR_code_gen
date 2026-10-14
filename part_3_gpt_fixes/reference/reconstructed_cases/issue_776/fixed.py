from qiskit.circuit import QuantumCircuit
from qiskit import Aer, execute

gamma, beta, zeta = 0.1, 0.2, 0.3


def my_circuit(initial_gate_params, params):
    circuit = QuantumCircuit(1)
    circuit.u3(initial_gate_params[0], initial_gate_params[1], initial_gate_params[2], 0)
    circuit.u3(params[0], params[1], params[2], 0)
    return circuit


initial_gate_params = [
    [0, 0, 0],
    [2, 3, 2],
    [-2.5, 2, -2]
]  # the params for your initial u3 gate

params = [gamma, beta, zeta]  # your defined gamma, beta, zeta

circuits = [my_circuit(i, params) for i in initial_gate_params]

backend = Aer.get_backend('qasm_simulator')
results = execute(circuits, backend)
