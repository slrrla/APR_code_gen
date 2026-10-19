from typing import Iterator
import numpy as np
import stim


def iter_pauli_strings(n: int) -> Iterator[stim.PauliString]:
    assert n <= 8
    for x in range(1 << n):
        for z in range(1 << n):
            yield stim.PauliString.from_numpy(
                xs=np.array([x], dtype=np.uint8),
                zs=np.array([z], dtype=np.uint8),
                num_qubits=n,
            )


def measure_pauli_product(simulator: stim.TableauSimulator, paulis: stim.PauliString) -> bool:
    targets = []
    for k, p in enumerate(paulis):
        if p == 1:
            t = stim.target_x
        elif p == 2:
            t = stim.target_y
        elif p == 3:
            t = stim.target_z
        else:
            continue
        targets.append(t(k))
        targets.append(stim.target_combiner())
    targets.pop()
    simulator.do(stim.CircuitInstruction(name='MPP', targets=targets))
    return simulator.current_measurement_record()[-1]


# Fixed: CY used instead of CZ followed by CX (avoids the phase kickback bug).
encoder = stim.Circuit("""
    H 0
    CX 0 4
    H 1
    CZ 1 0
    CY 1 4
    H 2
    CZ 2 1
    CY 2 4
    H 3
    CZ 3 0
    CZ 3 1
    CX 3 4
""")

stabilizers = [
    stim.PauliString("ZXZ_Y"),
    stim.PauliString("_ZXZY"),
    stim.PauliString("ZZ_XX"),
    stim.PauliString("X_ZZX"),
]

corrections = [
    stim.PauliString("+_____"),
    stim.PauliString("+Z____"),
    stim.PauliString("+___Z_"),
    stim.PauliString("+____Y"),
    stim.PauliString("+__Z__"),
    stim.PauliString("+___X_"),
    stim.PauliString("+_X___"),
    stim.PauliString("+___Y_"),
    stim.PauliString("+_Z___"),
    stim.PauliString("+__X__"),
    stim.PauliString("+X____"),
    stim.PauliString("+Y____"),
    stim.PauliString("+____X"),
    stim.PauliString("+__Y__"),
    stim.PauliString("+_Y___"),
    stim.PauliString("+____Z"),
]

max_error_weight = 1
num_qubits = 5
checked_qubits = [0, 1, 2, 3, 4]
any_failures = False

# Fixed: both X and Z logical observables are checked (via the four
# logical basis states 0, 1, +, -), not just the Z logical as before.
for state in '01+-':
    for err in iter_pauli_strings(num_qubits):
        if sum(p != 0 for p in err) > max_error_weight:
            continue

        sim = stim.TableauSimulator()

        if state == '0':
            init = stim.Circuit()
        elif state == '1':
            init = stim.Circuit("""
                X 4
            """)
        elif state == '+':
            init = stim.Circuit("""
                H 4
            """)
        elif state == '-':
            init = stim.Circuit("""
                H 4
                Z 4
            """)
        else:
            raise NotImplementedError(f'{state=}')

        sim.do(init)
        sim.do(encoder)

        # Apply chosen noise.
        sim.do(err)

        # Pick correction based on flipped stabilizers.
        fault_index = 0
        for stabilizer in stabilizers:
            fault_index *= 2
            fault_index += measure_pauli_product(sim, stabilizer)
        sim.do(corrections[fault_index])

        # caution: assumes each operation in the circuit is self-inverse
        sim.do(encoder[::-1])
        sim.do(init[::-1])

        if any(sim.measure_many(*checked_qubits)):
            print("Failed to correct", err, 'on logical state', state)
            any_failures = True

if not any_failures:
    print("All corrected")
