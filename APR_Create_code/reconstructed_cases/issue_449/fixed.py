from qiskit import QuantumCircuit

qc = QuantumCircuit(3)
qc.ccx(0, 1, 2)
qc = qc.decompose()

# Compute T-depth by filtering depth calculation to only T and Tdg gates
t_depth = qc.depth(lambda gate: gate[0].name in ['t', 'tdg'])
print('t depth:', t_depth)  # Output -> 4

qc.draw(output='mpl')
