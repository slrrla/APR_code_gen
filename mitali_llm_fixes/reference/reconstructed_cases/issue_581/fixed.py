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
    qc.measure_all()

    summand1 = 0
    for i in range(3):
        if l[i] == 1:
            summand1 += 2**(i)

    summand2 = 0
    for i in range(3):
        if l[i+3] == 1:
            summand2 += 2**(i)

    job = backend.run(transpile(qc, backend), shots=1024)
    res_dict = job.result().get_counts()
    res_sum = res_dict.most_frequent()

    sum = 0
    for i in range(3):
        if res_sum[i] == '1':
            sum += 2**(2-i)

    print(f"{summand1} + {summand2} = {sum}")
