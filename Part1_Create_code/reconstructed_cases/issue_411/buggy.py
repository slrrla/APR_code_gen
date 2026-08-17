from qiskit import transpile, assemble
from qiskit.providers.aer import AerSimulator
from qiskit.circuit.library import QuantumVolume
from IPython.display import clear_output

# --- setup: quantum volume circuits (as produced by the QV workflow) ---
n_qubits = 5
depth = 5
ntrials = 3

# each trial provides a *list* of circuits, as in the ignis/qiskit QV tutorial
qv_circs = [[QuantumVolume(n_qubits, depth, seed=trial)] for trial in range(ntrials)]
qubit_lists = [list(range(n_qubits))]

# use a local simulator instead of a real device
backend = AerSimulator()

shots = 1000
for trial in range(ntrials):
    clear_output(wait=True)
    t_qcs = transpile(qv_circs[trial], backend=backend, initial_layout=qubit_lists[0])
    qobj = [assemble(t_qcs)]  # BUG: wraps an already-assembled Qobj in a list
    job = backend.run(qobj, shots=shots)
    print(f'Completed trial {trial+1}/{ntrials}')
