import numpy as np
np.set_printoptions(threshold=np.inf)
import qiskit

backend = qiskit.Aer.get_backend('unitary_simulator')
qr = qiskit.QuantumRegister(4, name="qr")

CirA = qiskit.QuantumCircuit(qr)
CirA.cx(3, 2)
CirA.h(0)
CirA.cx(0, 2)
CirA.h(1)
CirA.cx(1, 3)
print(CirA)

job = qiskit.execute(CirA, backend, shots=1)
result = job.result()
MatA = result.get_unitary(CirA, 3)

CirB = qiskit.QuantumCircuit(qr)
CirB.unitary(MatA, [0, 1, 2, 3], label='CirB')
print(CirA)  # bug: should print CirB, not CirA again

unroller = qiskit.transpiler.passes.Unroller(basis=['u', 'cx'])
uCirA = qiskit.converters.dag_to_circuit(unroller.run(qiskit.converters.circuit_to_dag(CirA)))
print(uCirA)
uCirB = qiskit.converters.dag_to_circuit(unroller.run(qiskit.converters.circuit_to_dag(CirB)))
print(uCirB)
