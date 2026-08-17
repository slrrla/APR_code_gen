from multiprocessing import Pool
from qiskit import QuantumCircuit, Aer

def parallel(circ2):
    simulator2 = Aer.get_backend('aer_simulator')
    result2 = simulator.run(circ2).result()  # note: refers to undefined 'simulator' (typo in original)
    print(result2)

circ1 = QuantumCircuit(1)          # some kind of circuit
circ1.h(0)
circ1.measure_all()

simulator1 = Aer.get_backend('aer_simulator')
result1 = simulator1.run(circ1).result()
print(result1)

circs_arr = [circ1, circ1, circ1]  # some list of different circuits

if __name__ == '__main__':
    with Pool(5) as p:
        p.map(parallel, circs_arr)
