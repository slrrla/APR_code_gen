from qiskit import transpile
from qiskit.quantum_info import Statevector, state_fidelity
from qiskit.circuit.library import QFT
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime.fake_provider import FakeBrisbane

backend_brisbane = FakeBrisbane()

qc = QFT(6)

qc.remove_final_measurements()

ideal_sim = AerSimulator(method="statevector")

statevector_ideal = Statevector(qc)

qc_transpiled = transpile(qc, backend_brisbane, optimization_level=1)
# FIX: no save instruction in circuit (and full 127-qubit state is infeasible/mismatched) -> save the state of only the 6 logical qubits via final layout, because Aer only returns explicitly saved data and this matches the ideal 6-qubit state ordering
qc_transpiled.save_density_matrix(qubits=qc_transpiled.layout.final_index_layout())

job_real = ideal_sim.run(qc_transpiled)
# FIX: get_statevector() had nothing saved -> read the saved density matrix, because that is the data stored by the save instruction
statevector_real = job_real.result().data()["density_matrix"]

fidelity = state_fidelity(statevector_ideal, statevector_real)
print(f"Fidelity tra stato ideale e rumoroso: {fidelity:.4f}")
