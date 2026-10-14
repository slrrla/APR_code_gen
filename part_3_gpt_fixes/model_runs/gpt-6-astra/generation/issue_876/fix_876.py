from qiskit import transpile
from qiskit.quantum_info import Statevector, state_fidelity
from qiskit.circuit.library import QFT
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime.fake_provider import FakeBrisbane

backend_brisbane = FakeBrisbane()

qc = QFT(6)

qc.remove_final_measurements()

# FIX: The simulator was noiseless -> use the backend noise model and density-matrix simulation, because noisy states are generally mixed.
ideal_sim = AerSimulator.from_backend(backend_brisbane, method="density_matrix")

statevector_ideal = Statevector(qc)

qc_transpiled = transpile(qc, backend_brisbane, optimization_level=1)

# FIX: No state was saved and transpilation added physical qubits -> save only the logical output density matrix in logical order, because this excludes ancillas and lets Aer truncate idle qubits.
qc_transpiled.save_density_matrix(qubits=qc_transpiled.layout.final_index_layout())
job_real = ideal_sim.run(qc_transpiled)
# FIX: get_statevector requested an unsaved pure state -> retrieve the saved density matrix, because it represents the noisy output for fidelity comparison.
statevector_real = job_real.result().data(0)["density_matrix"]

fidelity = state_fidelity(statevector_ideal, statevector_real)
print(f"Fidelity tra stato ideale e rumoroso: {fidelity:.4f}")
