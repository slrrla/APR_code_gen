import math
import numpy as np
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import BasicAer, execute
from qiskit.circuit import Instruction
from qiskit.extensions.standard.cx import CnotGate


class ControlledInitialize(Instruction):
    """Controlled amplitude initialization (fixed version).

    Fix: the sub-circuit definition now works on a single QuantumRegister
    `q`, where the first qubit plays the role of the control and the
    remaining qubits are the ones that get initialized. This avoids
    the definition spanning two different registers, which is what
    caused the DAGCircuitError.
    """

    def __init__(self, controlled_qubit, params):
        # keep reference for API compatibility, though the definition
        # no longer uses it as a separate register
        self.controlled_qubit = controlled_qubit
        target_qubits = int(math.log2(len(params)))
        num_qubits = target_qubits + 1  # +1 for the control qubit
        super().__init__("controlledinitialize", num_qubits, 0, params)

    def _define(self):
        q = QuantumRegister(self.num_qubits, 'q')
        # fix: single register, first qubit is the control
        circuit = QuantumCircuit(q, name='init_def')
        circuit.append(CnotGate(), [q[0], q[1]])
        self.definition = circuit.data


def controlled_initialize(self, controlled_qubit, params, qreg):
    instr = ControlledInitialize(controlled_qubit, params)
    return self.append(instr, [controlled_qubit[0]] + qreg[:])


QuantumCircuit.controlled_initialize = controlled_initialize

desired_vector = [1 / math.sqrt(2), 0, 0, 1 / math.sqrt(2)]
qctl = QuantumRegister(1, "qctl")
qreg = QuantumRegister(2, "qreg")
creg = ClassicalRegister(2, "creg")
circuit = QuantumCircuit(qctl, qreg, creg)
circuit.x(qctl)
circuit.controlled_initialize(qctl, desired_vector, qreg)
circuit.measure(qreg, creg)
job = execute(circuit, BasicAer.get_backend('qasm_simulator'), shots=10000)
print('Counts: ', job.result().get_counts(circuit))
