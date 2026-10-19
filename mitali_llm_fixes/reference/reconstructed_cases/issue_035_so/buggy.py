from qiskit_ibm_runtime import QiskitRuntimeService, Sampler
from qiskit import QuantumCircuit

service = QiskitRuntimeService(
    channel='ibm_quantum',
    instance='ibm-q/open/main',
)

bell = QuantumCircuit(2, 1)
res = bell.qregs[0]
cr = bell.cregs[0]
bell.h(0)
bell.x(res[0]).c_if(cr, 0)
bell.cx(0, 1)
bell.x(res[1]).c_if(cr, 0)
bell.measure_all()

# executes three Bell circuits
# BUG: qiskit_ibm_runtime's Sampler primitive cannot run dynamic circuits
# (there is no way to pass dynamic=True to the Runtime backend here)
with Sampler(
    circuits=[bell] * 3,
    service=service,
    options={'backend': 'ibmq_qasm_simulator'},
) as sampler:
    # alternatively you can also pass circuits as objects
    result = sampler(circuits=[bell] * 3)
    print(result)
