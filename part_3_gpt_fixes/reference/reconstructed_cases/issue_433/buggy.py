import numpy as np
import numpy.testing as npt
from qiskit import QuantumCircuit
from qiskit.quantum_info.operators import Operator
from qiskit.extensions import UnitaryGate


def test1():
    oneone = np.array([[0, 0], [0, 1]])
    zerozero = np.array([[1, 0], [0, 0]])
    eye = np.identity(2)
    unitary = np.array([[0, 1], [1, 0]])

    # manual construction using numpy Kronecker product
    cx = np.kron(zerozero, eye) + np.kron(oneone, unitary)

    op_auto = UnitaryGate(unitary).control(1, ctrl_state='1')
    qc1 = QuantumCircuit(2)
    # Passes only due to reversed ordering of qubits.
    qc1.append(op_auto, [1, 0])
    op_auto = Operator.from_circuit(qc1)

    op_manual = UnitaryGate(cx)
    qc2 = QuantumCircuit(2)
    qc2.append(op_manual, [0, 1])
    op_manual = Operator.from_circuit(qc2)

    npt.assert_array_almost_equal(op_auto.data, op_manual.data)


test1()
