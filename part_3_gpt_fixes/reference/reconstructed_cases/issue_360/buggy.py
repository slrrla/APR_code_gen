from qiskit import *


def uppg(inp1, inp2, inp3, inp4):
    qc = QuantumCircuit(4, 4)
    # conditions
    if inp1 == '1':
        qc.x(0)
    if inp2 == '1':
        qc.x(1)
    if inp3 == '1':
        qc.x(2)
    if inp4 == '1':
        qc.x(3)
    qc.barrier()
    # circuit
    qc.cx(3, 1)
    qc.cx(1, 0)
    qc.cx(0, 1)
    qc.ccx(3, 2, 1)
    qc.cx(1, 2)
    qc.cx(3, 2)
    # measure
    qc.measure(0, 3)
    qc.measure(1, 2)
    qc.measure(2, 1)
    qc.measure(3, 0)
    qc.draw()
    # backend
    backend = Aer.get_backend('qasm_simulator')
    job = execute(qc, backend, memory=True)
    output = job.result().get_memory()[0]
    return qc, output


for inp1 in ['0', '1']:
    for inp2 in ['0', '1']:
        for inp3 in ['0', '1']:
            for inp4 in ['0', '1']:
                qc_new, output = uppg(inp1, inp2, inp3, inp4)
                print('{} {} {} {}'.format(inp1, inp2, inp3, inp4), '=', output)
                print(qc_new.draw())
