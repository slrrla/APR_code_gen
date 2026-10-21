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

# FIX: transpiled for 127-qubit hardware and no statevector saved -> transpile for the simulator and call save_statevector(), because the result only contains a statevector if one is saved and the 6-qubit circuit stays small
qc_transpiled = transpile(qc, ideal_sim, optimization_level=1)
qc_transpiled.save_statevector()

job_real = ideal_sim.run(qc_transpiled)
statevector_real = job_real.result().get_statevector()

fidelity = state_fidelity(statevector_ideal, statevector_real)
print(f"Fidelity tra stato ideale e rumoroso: {fidelity:.4f}")
