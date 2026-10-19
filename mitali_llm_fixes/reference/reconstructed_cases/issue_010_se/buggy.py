from concurrent.futures import ThreadPoolExecutor, as_completed

from qiskit import QuantumCircuit


def run_circuit(circuit):
    return {"name": circuit.name, "counts": {"0": 1024}}


circuits = []
for i in range(4):
    qc = QuantumCircuit(1, 1, name=f"circuit_{i}")
    qc.measure(0, 0)
    circuits.append(qc)

with ThreadPoolExecutor(max_workers=4) as pool:
    futures = [pool.submit(run_circuit, qc) for qc in circuits]
    results = [future.result() for future in as_completed(futures)]

for circuit, result in zip(circuits, results):
    print(circuit.name, result["name"])
