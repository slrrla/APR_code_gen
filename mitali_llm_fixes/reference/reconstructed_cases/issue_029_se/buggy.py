from qiskit import QuantumRegister

# Trying to create sub-registers from slices of an existing register's qubits.
# QuantumRegister does not accept qubits as constructor argument this way.
axreg = QuantumRegister(4, name='ax')
ahreg = QuantumRegister(axreg[:2], name='ah')
alreg = QuantumRegister(axreg[2:], name='al')
