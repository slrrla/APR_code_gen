import itertools
import math
import qiskit


def Test():
    backend = qiskit.Aer.get_backend('qasm_simulator')
    n = 5
    k = 1
    m = 4
    t = 1
    qr = qiskit.QuantumRegister(n + m, name="qr")
    cr = qiskit.ClassicalRegister(n + m, name="cr")

    # 5-qubit code encoder.  NOTE: uses CZ followed by CX instead of CY -
    # this is the bug reported (creates an unwanted phase kickback).
    qcenc = qiskit.QuantumCircuit(qr, cr)
    qcenc.h(0); qcenc.cx(0, 4)
    qcenc.h(1); qcenc.cz(1, 0); qcenc.cz(1, 4); qcenc.cx(1, 4)
    qcenc.h(2); qcenc.cz(2, 1); qcenc.cz(2, 4); qcenc.cx(2, 4)
    qcenc.h(3); qcenc.cz(3, 0); qcenc.cz(3, 1); qcenc.cx(3, 4)
    qcenc.barrier()

    qcsyn = qiskit.QuantumCircuit(qr, cr)
    qcsyn.h(5); qcsyn.h(6); qcsyn.h(7); qcsyn.h(8)
    qcsyn.cx(5, 0); qcsyn.cz(5, 2); qcsyn.cz(5, 3); qcsyn.cx(5, 4)
    qcsyn.cz(6, 0); qcsyn.cz(6, 1); qcsyn.cx(6, 1); qcsyn.cz(6, 2); qcsyn.cz(6, 4); qcsyn.cx(6, 4)
    qcsyn.cz(7, 1); qcsyn.cz(7, 2); qcsyn.cx(7, 2); qcsyn.cz(7, 3); qcsyn.cz(7, 4); qcsyn.cx(7, 4)
    qcsyn.cz(8, 0); qcsyn.cz(8, 1); qcsyn.cx(8, 3); qcsyn.cx(8, 4)
    qcsyn.h(5); qcsyn.h(6); qcsyn.h(7); qcsyn.h(8)
    qcsyn.barrier()

    # Correction circuit (abridged): a controlled gate keyed on the 4
    # syndrome qubits, applying a Pauli correction on the code qubits.
    qccor = qiskit.QuantumCircuit(qr, cr)
    gate = qiskit.QuantumCircuit(5)
    gate.x(0)
    qccor.append(gate.control(num_ctrl_qubits=4), [5, 6, 7, 8, 0, 1, 2, 3, 4])
    qccor.barrier()

    qcenx = qcenc.inverse()

    WrdNum = 0
    WrdErr = 0
    locs = itertools.combinations(range(n), t)
    for i in range(math.comb(n, t)):
        loc = next(locs)
        errs = itertools.product([0, 1, 2], repeat=t)
        for j in range(3 ** t):
            err = next(errs)
            # NOTE: only computational-basis (Z logical) inputs are tried,
            # the X logical observable is never checked - second part of the bug.
            TxBits = itertools.product([0, 1], repeat=k)
            for h in range(2 ** k):
                txbits = next(TxBits)
                qcini = qiskit.QuantumCircuit(qr, cr)
                for ii in range(k):
                    if txbits[ii] == 1:
                        qcini.x(m + ii)
                    else:
                        qcini.z(m + ii)

                chn = qiskit.QuantumCircuit(qr)
                for kk in range(t):
                    if err[kk] == 0:
                        chn.x(loc[kk])
                    if err[kk] == 1:
                        chn.z(loc[kk])
                    if err[kk] == 2:
                        chn.y(loc[kk])
                chn.barrier()

                qc = qcini + qcenc + chn + qcsyn + qccor + qcenx
                for ii in range(n + m):
                    qc.measure(qr[ii], cr[ii])

                job = qiskit.execute(qc, backend, shots=1)
                result = job.result()
                counts = result.get_counts(qc)
                Counts = [(kx[::-1], v) for kx, v in counts.items()]
                rxbits = []
                for kx, v in Counts:
                    rxbits.append([int(c) for c in kx])

                WrdNum += 1
                werr = 0
                for ii in range(k):
                    if rxbits[0][m + ii] != txbits[ii]:
                        werr = 1
                WrdErr += werr
                print("tx=", txbits, "rx=", rxbits[0][m:m + k],
                      "err loc=", loc, "err val=", err,
                      "decoding errors=", WrdErr, "/", WrdNum)


if __name__ == "__main__":
    Test()
