from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_ibm_runtime import SamplerV2

qr = QuantumRegister(3, "q")
cr0 = ClassicalRegister(2, "c_reg0")
cr1 = ClassicalRegister(2, "c_reg1")
qc = QuantumCircuit(qr, cr0, cr1)
qc.h(0)
qc.cx(0, 1)
qc.measure(0, cr0[0])
qc.measure(1, cr0[1])
qc.h(2)
qc.measure(2, cr1[0])

sampler = SamplerV2()
job = sampler.run([qc])
result = job.result()[0]

# messy per-register access, and no combined counts available
counts_c_reg0 = result.data.c_reg0.get_counts()
