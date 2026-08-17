from qiskit_ibm_provider import Session
from qiskit.primitives import BackendSampler
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

# Use a local simulator standing in for the IBM provider backend
backend = AerSimulator()
backend.options.dynamic = True  # enable dynamic circuits on the backend

bell = QuantumCircuit(2, 1)
res = bell.qregs[0]
cr = bell.cregs[0]
bell.h(0)
bell.x(res[0]).c_if(cr, 0)
bell.cx(0, 1)
bell.x(res[1]).c_if(cr, 0)
bell.measure_all()

# Wrap backend.run inside a Session and use BackendSampler,
# which supports dynamic circuits (unlike qiskit_ibm_runtime's Sampler)
with Session(backend=backend):
    sampler = BackendSampler(backend=backend)
    result = sampler.run(circuits=[bell] * 3).result()
    print(result)
