from qiskit import QuantumCircuit, Aer, execute, QuantumRegister, ClassicalRegister

num = 4

def reset(n):
    a = QuantumRegister(n, 'a')
    qc = QuantumCircuit(a)
    qc.reset(0)
    name = "reset"
    qc_reset = qc.to_gate()          # fails: reset is not a gate instruction
    reset_qubit = qc.control(1)
    return reset_qubit

a = QuantumRegister(num, 'a')
qc = QuantumCircuit(a)
qc.append(reset(num), range(num))
