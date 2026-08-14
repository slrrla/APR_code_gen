from qiskit import *
from qiskit.visualization import array_to_latex
from qiskit_experiments.library import StateTomography
from qiskit.providers.fake_provider import FakeManilaV2

backend = FakeManilaV2()

q1 = QuantumRegister(1)
q2 = QuantumRegister(1)
q3 = QuantumRegister(1)
c = ClassicalRegister(3)
qc = QuantumCircuit(q1, q2, q3, c)
qc.h(q1)
qc.cx(q1, q2)
qc.ccx(q1, q2, q3)

st = StateTomography(qc, physical_qubits=[90, 94, 95])

stdata = st.run(backend).block_for_results()
state_result = stdata.analysis_results("state")
array_to_latex(state_result.value)
fid_result = stdata.analysis_results("state_fidelity")
print(f"state Fidelity = {fid_result.value}")

# Verify which qubits were actually used
from qiskit.visualization import plot_circuit_layout
plot_circuit_layout(st._transpiled_circuits()[0], backend=backend, view='physical')
