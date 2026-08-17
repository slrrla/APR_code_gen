import itertools
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.circuit.library import DraperQFTAdder

backend = AerSimulator()
adder = DraperQFTAdder(3).decompose()

for l in list(itertools.product([0, 1], repeat=6)):
    qc = QuantumCircuit(6)
    for i, bit in enumerate(l):
        if bit == 1:
            qc.x(i)
    qc.append(adder, [0, 1, 2, 3, 4, 5])
    qc = qc.reverse_bits()
    qc.measure_all()
    job = backend.run(transpile(qc, backend), shots=1024)
    print(f"Input: {l}. Result: {job.result().get_counts()}")
