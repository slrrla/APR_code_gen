import qiskit
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer
import numpy as np
from qiskit.aqua import QuantumInstance
from qiskit.aqua.operators import PauliExpectation, CircuitSampler, StateFn, CircuitOp, CircuitStateFn

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

# Bug: trying to batch multiple circuits by submitting them individually
# via IBMQJobManager instead of using ListOp, which does not work with
# the aqua expectation value operator logic as constructed here.
measurable_expression1 = StateFn(op1, is_measurement=True).compose(psi)
expectation1 = PauliExpectation().convert(measurable_expression1)
sampler1 = CircuitSampler(q_instance).convert(expectation1)
print('Expectation Value 1 = ', sampler1.eval())

measurable_expression2 = StateFn(op2, is_measurement=True).compose(psi)
expectation2 = PauliExpectation().convert(measurable_expression2)
sampler2 = CircuitSampler(q_instance).convert(expectation2)
print('Expectation Value 2 = ', sampler2.eval())

IBMQJobManager()
