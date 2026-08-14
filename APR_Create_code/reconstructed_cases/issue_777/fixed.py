import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit.library import PauliEvolutionGate

def quantum_state_preparation(sites, reps):
    qc = QuantumCircuit(sites)
    num_params = reps*(2*sites+1)
    params = ParameterVector('θ', num_params)
    H = 0*SparsePauliOp('I'*(sites))
    for j in range(1, sites):
        H -= 1/2 * (SparsePauliOp('I'*(j-1) + 'XX' + 'I'*(sites-j-1)) + SparsePauliOp('I'*(j-1) + 'YY' + 'I'*(sites-j-1)))
    ham_op = H.simplify()
    for n in range(reps):
        # PauliEvolutionGate supports unbound Parameters, unlike HamiltonianGate
        ham_gate = PauliEvolutionGate(ham_op, time=params[n*(2*sites+1)]/2)
        qc.append(ham_gate, range(sites))
        for i in range(sites):
            # single qubit gates
            qc.p(params[n*(2*sites+1)+1+2*i], i)
            qc.rx(params[n*(2*sites+1)+2+2*i], i)
    qc.parameter_bounds = [[0, 2*np.pi]]*num_params
    return qc

if __name__ == "__main__":
    circ = quantum_state_preparation(sites=4, reps=1)
    print(circ)
