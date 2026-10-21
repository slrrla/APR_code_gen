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

# FIX: transpiling to the full 127-qubit device made the statevector too big and not comparable with the 6-qubit ideal state -> transpile only to the device's basis gates, because this keeps the circuit at 6 qubits in the same order while still using the hardware gate set
qc_transpiled = transpile(qc, basis_gates=list(backend_brisbane.operation_names), optimization_level=1)
# FIX: missing save instruction caused "No statevector for experiment" -> added save_statevector(), because AerSimulator only returns a statevector when the circuit explicitly saves it
qc_transpiled.save_statevector()

job_real = ideal_sim.run(qc_transpiled)
statevector_real = job_real.result().get_statevector()

fidelity = state_fidelity(statevector_ideal, statevector_real)
print(f"Fidelity tra stato ideale e rumoroso: {fidelity:.4f}")
