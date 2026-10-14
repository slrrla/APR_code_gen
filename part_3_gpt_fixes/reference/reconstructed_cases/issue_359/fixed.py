from qiskit import QuantumCircuit, Aer, assemble, execute
from qiskit.visualization import array_to_latex

qc = QuantumCircuit(2)
qc.h(0)
qc.h(1)

# First way to get statevector: using save_statevector with a label + assemble
svsim = Aer.get_backend('aer_simulator')
qc.save_statevector(label='sv')
qobj = assemble(qc)
final_state = svsim.run(qobj).result().data()['sv']

# Now to display it
array_to_latex(final_state, prefix="|\\psi^{AB} \\rangle = ")

# Second way to get statevector: using statevector_simulator with execute
backend = Aer.get_backend('statevector_simulator')
result = execute(qc, backend).result()
out_state = result.get_statevector()
array_to_latex(out_state, prefix="|\\psi^{AB} \\rangle = ")
