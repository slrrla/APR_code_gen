import qiskit
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer
import numpy as np
from qiskit.aqua import QuantumInstance
from qiskit.aqua.operators import PauliExpectation, CircuitSampler, StateFn, CircuitOp, CircuitStateFn, ListOp

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

# Bug: trying to batch multiple circuits by submitting them individually
# via IBMQJobManager instead of using ListOp, which does not work with
# the aqua expectation value operator logic as constructed here.
measurable_expressions = ListOp([
    StateFn(op1, is_measurement=True).compose(psi),
    StateFn(op2, is_measurement=True).compose(psi),
])
expectations = PauliExpectation().convert(measurable_expressions)
sampler = CircuitSampler(q_instance).convert(expectations)
expectation_values = sampler.eval()
print('Expectation Value 1 = ', expectation_values[0])
print('Expectation Value 2 = ', expectation_values[1])
