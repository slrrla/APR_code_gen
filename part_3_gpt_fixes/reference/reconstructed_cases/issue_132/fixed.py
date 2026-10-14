from qiskit import QuantumCircuit, execute, Aer, assemble, QuantumRegister, ClassicalRegister

qc = QuantumCircuit(2, 2)
qc.h(0)
# qc.measure(0, 0)  # measurement removed so statevector isn't collapsed
qc.x(1)
qc.h(1)
# qc.measure(1, 1)  # measurement removed so statevector isn't collapsed
qc.draw(output="mpl")

svsim = Aer.get_backend('aer_simulator')
qc.save_statevector()
qobj = assemble(qc)
final_state = svsim.run(qobj).result().get_statevector(decimals=3)

from qiskit.visualization import array_to_latex, plot_bloch_multivector
array_to_latex(final_state, prefix="\\text{Statevector} = ")
plot_bloch_multivector(final_state)
