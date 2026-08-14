from qiskit import QuantumCircuit, execute, Aer, assemble, QuantumRegister, ClassicalRegister

qc = QuantumCircuit(2, 2)
qc.h(0)
qc.measure(0, 0)
qc.x(1)
qc.h(1)
qc.measure(1, 1)
qc.draw(output="mpl")

svsim = Aer.get_backend('aer_simulator')
qc.save_statevector()
qobj = assemble(qc)
final_state = svsim.run(qobj).result().get_statevector(decimals=3)

from qiskit.visualization import array_to_latex
array_to_latex(final_state, prefix="\\text{Statevector} = ")
