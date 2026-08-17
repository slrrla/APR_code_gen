import numpy as np
from qiskit.circuit.library import RealAmplitudes
from qiskit.quantum_info import SparsePauliOp
from qiskit_ibm_runtime import Session, Options, Estimator

psi1 = RealAmplitudes(5, reps=2)
H1 = SparsePauliOp.from_list([("XZ", 1), ("YY", 3)])
theta1 = np.linspace(0, 1, 5 * 3)

with Session(service=service, backend=backend):
    options = Options(simulator={"seed_simulator": 42}, resilience_level=0)
    estimator = Estimator(options=options)
    job = estimator.run(circuits=[psi1], parameter_values=[list(theta1)], observables=[H1])
    result = job.result()
