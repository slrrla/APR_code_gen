import qiskit
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer
import numpy as np
from qiskit.aqua import QuantumInstance
from qiskit.aqua.operators import PauliExpectation, CircuitSampler, StateFn, CircuitOp, CircuitStateFn, ListOp

qctl = QuantumRegister(1)
psi = QuantumCircuit(qctl)
psi = CircuitStateFn(psi)

qctl = QuantumRegister(2)
op1 = QuantumCircuit(qctl)
op1.z(0)
op1.ry(np.pi/4, 0)
op1 = CircuitOp(op1)

qctl = QuantumRegister(2)
op2 = QuantumCircuit(qctl)
op2.x(0)
op2.ry(np.pi/3, 0)
op2 = CircuitOp(op2)

backend = Aer.get_backend('qasm_simulator')
q_instance = QuantumInstance(backend, shots=1024)

# Fix: collect the circuits into a list and wrap them with ListOp so that
# CircuitSampler assembles them into a single batched payload for the backend.
ops = []
# ... Construct your first circuit ...
# Now, add it to the list:
ops.append(op1)
# ... Construct your second circuit ...
# Now, add it to the list:
ops.append(op2)

measurable_expression = StateFn(ListOp(ops), is_measurement=True).compose(psi)
expectation = PauliExpectation().convert(measurable_expression)
sampler = CircuitSampler(q_instance).convert(expectation)
print('Expectation Value = ', sampler.eval())
