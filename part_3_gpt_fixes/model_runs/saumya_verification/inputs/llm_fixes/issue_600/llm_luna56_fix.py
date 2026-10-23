import qiskit
from qiskit import QuantumRegister, ClassicalRegister, transpile, execute, Aer
from qiskit.circuit.library import PauliGate
# FIX: PauliGate.power evaluates powers numerically -> import a gate supporting symbolic evolution times, because ParameterVectorElement cannot be used by PauliGate.power
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.quantum_info import Pauli
import numpy as np


class MyQuantumCircuit:
    def __init__(self, backend, shots=100):
        self._q = QuantumRegister(3, 'q')
        self._c = ClassicalRegister(1, 'c')
        self._circuit = qiskit.QuantumCircuit(self._q, self._c)
        self.inp = qiskit.circuit.ParameterVector('inp', 2)
        self.param = qiskit.circuit.ParameterVector('param', 6)

        self._circuit.rx(self.inp[0], 0)
        self._circuit.rx(self.inp[1], 1)

        # FIX: PauliGate.power cannot raise a gate to a symbolic exponent -> use equivalent parameterized Pauli evolution, because it supports ParameterVectorElement
        xx10 = PauliEvolutionGate(Pauli('XX'), time=np.pi * self.param[0] / 2)
        xx11 = PauliEvolutionGate(Pauli('XX'), time=np.pi * self.param[1] / 2)
        self._circuit.append(xx10, [0, 2])
        self._circuit.append(xx11, [1, 2])

        # FIX: PauliGate.power cannot raise a gate to a symbolic exponent -> use equivalent parameterized Pauli evolution, because it supports ParameterVectorElement
        yy10 = PauliEvolutionGate(Pauli('YY'), time=np.pi * self.param[2] / 2)
        yy11 = PauliEvolutionGate(Pauli('YY'), time=np.pi * self.param[3] / 2)
        self._circuit.append(yy10, [0, 2])
        self._circuit.append(yy11, [1, 2])

        # FIX: PauliGate.power cannot raise a gate to a symbolic exponent -> use equivalent parameterized Pauli evolution, because it supports ParameterVectorElement
        zz10 = PauliEvolutionGate(Pauli('ZZ'), time=np.pi * self.param[4] / 2)
        zz11 = PauliEvolutionGate(Pauli('ZZ'), time=np.pi * self.param[5] / 2)
        self._circuit.append(zz10, [0, 2])
        self._circuit.append(zz11, [1, 2])

        self._circuit.measure(2, 0)
        self.backend = backend
        self.shots = shots

    def run(self, inp, theta):
        qc = transpile(self._circuit, self.backend)
        bind_dict = {}
        j = 0
        k = 0
        for key in qc.parameters:
            if j <= 1:
                bind_dict[key] = inp[j]
                j += 1
            else:
                bind_dict[key] = theta[k]
                k += 1
        qc.assign_parameters(bind_dict, inplace=True)
        job = execute(qc, self.backend, shots=self.shots)
        result = job.result()
        c = result.get_counts()
        states = np.array(list(c.keys())).astype(float)
        counts = np.array(list(c.values())).astype(int)
        dist = counts / self.shots
        E = np.array([np.sum(states * dist)])
        return E


backend = Aer.get_backend('qasm_simulator')
circ = MyQuantumCircuit(backend, shots=10)
inp = np.array([0.50002703, 0.56683592])
theta = np.array([2.37624305, 5.00052773, 1.60817906, 1.01813369, 1.36693303, 2.58211921])
print(circ.run(inp, theta))
