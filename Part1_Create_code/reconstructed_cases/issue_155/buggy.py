from qiskit import Aer, QuantumCircuit, QuantumRegister, transpile
from qiskit.quantum_info import partial_trace

qc = QuantumCircuit()
reg1 = QuantumRegister(2)
qc.add_register(reg1)
reg2 = QuantumRegister(2)
qc.add_register(reg2)
reg3 = QuantumRegister(2)
qc.add_register(reg3)
reg4 = QuantumRegister(2)
qc.add_register(reg4)

# It's not relevant to the question what exactly is done in the circuit
qc.h(reg1[0])
qc.cnot(reg1[0], reg2[0])
qc.h(reg3[0])
qc.x(reg4[0])
qc.cnot(reg3[0], reg4[0])

simulator = Aer.get_backend("aer_simulator")
qc.save_statevector()
transpiled_qc = transpile(qc, simulator)
result = simulator.run(transpiled_qc).result()

# BUG: passing QuantumRegister objects directly to partial_trace instead of qubit indices
traced_over_registers = [reg2, reg4]
density_matrix = partial_trace(result.get_statevector(), traced_over_registers)
