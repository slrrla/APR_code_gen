# imports
from qiskit import transpile
from qiskit.quantum_info import Statevector, state_fidelity
from qiskit.circuit.library import QFT
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime.fake_provider import FakeBrisbane

# local stand-in for a real backend (no network calls)
backend_brisbane = FakeBrisbane()

# build QFT circuit
qc = QFT(6)

# to be sure there is no measurement
qc.remove_final_measurements()

# ideal simulator for the "clean" statevector
ideal_sim = AerSimulator(method="statevector")

# Ideal SV obtained as before
statevector_ideal = Statevector(qc)

# transpile my QFT circuit based on real hardware
qc_transpiled = transpile(qc, backend_brisbane, optimization_level=1)

# get SV with real hardware noise using AerSimulator
job_real = ideal_sim.run(qc_transpiled)
statevector_real = job_real.result().get_statevector()

# Compare them
fidelity = state_fidelity(statevector_ideal, statevector_real)
print(f"Fidelity tra stato ideale e rumoroso: {fidelity:.4f}")
