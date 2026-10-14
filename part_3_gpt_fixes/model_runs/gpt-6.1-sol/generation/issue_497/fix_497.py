import qiskit
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer
import numpy as np
from qiskit.aqua import QuantumInstance
# FIX: Separate expectations were not grouped -> import ListOp, because CircuitSampler can batch its contained expectations.
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

measurable_expression1 = StateFn(op1, is_measurement=True).compose(psi)
expectation1 = PauliExpectation().convert(measurable_expression1)
# FIX: The second expectation was built after sampling the first -> build it before sampling, because both must be available for batching.
measurable_expression2 = StateFn(op2, is_measurement=True).compose(psi)
expectation2 = PauliExpectation().convert(measurable_expression2)
# FIX: Separate CircuitSampler conversions submitted separate executions -> convert one ListOp and unpack its results, because this batches both expectations.
sampler1, sampler2 = CircuitSampler(q_instance).convert(ListOp([expectation1, expectation2])).oplist
print('Expectation Value 1 = ', sampler1.eval())

print('Expectation Value 2 = ', sampler2.eval())

# FIX: IBMQJobManager() was undefined and did not submit any circuits -> remove the call, because CircuitSampler already executes the batched expectations.
