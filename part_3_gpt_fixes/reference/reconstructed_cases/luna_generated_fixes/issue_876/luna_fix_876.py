from qiskit import transpile
from qiskit.quantum_info import Statevector, state_fidelity
from qiskit.circuit.library import QFT
from qiskit_aer import AerSimulator
from qiskit.ibm_runtime.fake_provider import FakeBrisbane

backend_brisbane = FakeBrisbane()

qc = QFT(6)

qc.remove_final_measurements()

ideal_sim = AerSimulator(method="statevector")

statevector_ideal = Statevector(qc)

qc_transpiled = transpile(qc, backend_brisbane, optimization_level=1)

# FIX: the circuit did not request a saved statevector -> add the save instruction, because AerSimulator only returns statevectors that are explicitly saved
qc_transpiled.save_statevector()

job_real = ideal_sim.run(qc_transpiled)
statevector_real = job_real.result().get_statevector()

fidelity = state_fidelity(statevector_ideal, statevector_real)
print(f"Fidelity tra stato ideale e rumoroso: {fidelity:.4f}")
