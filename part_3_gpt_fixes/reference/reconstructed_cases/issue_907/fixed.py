from qiskit.circuit.library import RealAmplitudes

ansatz = RealAmplitudes(3, reps=2)
print(ansatz.decompose())
