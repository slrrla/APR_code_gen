from qiskit import QuantumCircuit, execute, Aer
# FIX: duplicate import from removed/deprecated qiskit.providers.ibmq.job (which also shadowed this one) -> deleted it and kept only qiskit.tools.monitor, because the generic monitor works for any backend job and the ibmq module is not available
from qiskit.tools.monitor import job_monitor

qc = QuantumCircuit(1, 1)
qc.h(0)
qc.measure(0, 0)

backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend)

job_monitor(job)
