import math
import numpy as np
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import BasicAer, execute
from qiskit.circuit import Instruction
from qiskit.extensions.standard.cx import CnotGate


class ControlledInitialize(Instruction):
    """Controlled amplitude initialization (buggy version).

    WATCH ME: controlled_qubit is stored separately and used as its own
    QuantumRegister inside the sub-circuit definition, together with a
    second, locally created register `q`. This is the bug: the definition
    ends up spanning two distinct registers instead of one, and when the
    instruction is later decomposed the DAG can't find the qubits of the
    original `qctl` register inside the local sub-circuit context.
    """

    def __init__(self, controlled_qubit, params):
        # WATCH ME: save controlled qubit register
        self.controlled_qubit = controlled_qubit
        target_qubits = int(math.log2(len(params)))
        num_qubits = target_qubits + 1  # +1 for the control qubit
        super().__init__("controlledinitialize", num_qubits, 0, params)

    def _define(self):
        q = QuantumRegister(self.num_qubits - 1, 'q')
        # WATCH ME: sub-circuit built on two separate registers
        circuit = QuantumCircuit(self.controlled_qubit, q, name='init_def')
        circuit.append(CnotGate(), [self.controlled_qubit[0], q[0]])
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
