from qiskit import Aer

# Reproduces: ImportError: cannot import name 'Aer' from 'qiskit'
backend = Aer.get_backend('qasm_simulator')
