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

# Keep the two expectation computations together so CircuitSampler can submit
# their measurement circuits in a single backend execution.
measurable_expression1 = StateFn(op1, is_measurement=True).compose(psi)
measurable_expression2 = StateFn(op2, is_measurement=True).compose(psi)
expressions = ListOp([measurable_expression1, measurable_expression2])
expectations = PauliExpectation().convert(expressions)
values = CircuitSampler(q_instance).convert(expectations).eval()
print('Expectation Value 1 = ', values[0])
print('Expectation Value 2 = ', values[1])
