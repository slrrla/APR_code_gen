import qiskit
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer
import numpy as np
from qiskit.aqua import QuantumInstance
# FIX: ListOp was missing -> import it, because multiple expectation operators must be combined for one batch
from qiskit.aqua.operators import PauliExpectation, CircuitSampler, StateFn, CircuitOp, CircuitStateFn, ListOp

# FIX: the state and operators had different qubit counts -> use two qubits, because composition requires matching dimensions
qctl = QuantumRegister(2)
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

measurable_expression1 = StateFn(op1, is_measurement=True).compose(psi)
expectation1 = PauliExpectation().convert(measurable_expression1)

measurable_expression2 = StateFn(op2, is_measurement=True).compose(psi)
expectation2 = PauliExpectation().convert(measurable_expression2)

# FIX: the expectation values were evaluated in separate jobs -> combine them, because CircuitSampler can batch the circuits
expectations = ListOp([expectation1, expectation2])
sampler = CircuitSampler(q_instance).convert(expectations)
values = sampler.eval()
print('Expectation Value 1 = ', values[0])
print('Expectation Value 2 = ', values[1])

# FIX: IBMQJobManager was undefined and unused -> remove it, because CircuitSampler handles the batch execution
