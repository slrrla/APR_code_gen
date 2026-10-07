from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

# Simple circuit without classical register
circuit = QuantumCircuit(1)
circuit.h(0)

backend = AerSimulator(method='unitary')
job = backend.run(circuit).result()

# Check what attributes the result object has
print("Result object type:", type(job))
print("\nChecking result dict:")
result_dict = job.to_dict()
print("Result dict keys:", result_dict.keys())

# Look at the experiments
print("\nExperiments:", result_dict.get('results'))

# Try to see what the raw result looks like
for i, res in enumerate(result_dict.get('results', [])):
    print(f"\nExperiment {i}:")
    print("Keys:", res.keys() if isinstance(res, dict) else dir(res))
    if isinstance(res, dict):
        if 'data' in res:
            print("Data:", res['data'])
