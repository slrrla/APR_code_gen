from typing import Union, List
import stim


def bit_row_to_pauli_strings(row: List[Union[int, bool]]) -> stim.PauliString:
    n = len(row) // 2
    assert n * 2 == len(row)
    out = stim.PauliString(n)
    for k in range(n):
        pauli = row[k] + row[k + n] * 2
        if pauli >= 2:
            # switch from Z=2 Y=3 to Y=2 Z=3
            pauli ^= 1
        out[k] = pauli
    return out


def bit_matrix_to_tableau(matrix: List[List[Union[int, bool]]]) -> stim.Tableau:
    n = len(matrix) // 2
    assert n * 2 == len(matrix)
    pauli_strings = [bit_row_to_pauli_strings(row) for row in matrix]
    return stim.Tableau.from_conjugated_generators(
        xs=pauli_strings[n:],
        zs=pauli_strings[:n],
    )


def tableau_to_circuit_simple(tableau: stim.Tableau) -> stim.Circuit:
    remaining = tableau.inverse()
    recorded_circuit = stim.Circuit()

    def do(gate: str, targets: List[int]):
        recorded_circuit.append(gate, targets)
        remaining.append(stim.Tableau.from_named_gate(gate), targets)

    n = len(remaining)
    for col in range(n):
        # Find a cell with an anti-commuting pair of Paulis.
        for pivot_row in range(col, n):
            px = remaining.x_output_pauli(col, pivot_row)
            pz = remaining.z_output_pauli(col, pivot_row)
            if px and pz and px != pz:
                break
        else:
            raise NotImplementedError("Failed to find a pivot cell")

        # Move the pivot to the diagonal.
        if pivot_row != col:
            do("SWAP", [pivot_row, col])

        # Transform the pivot to XZ.
        px = remaining.x_output_pauli(col, col)
        if px == 3:
            do("H", [col])
        elif px == 2:
            do("H_XY", [col])
        pz = remaining.z_output_pauli(col, col)
        if pz == 2:
            do("H_YZ", [col])

        # Use the pivot to remove all other terms in the X observable.
        for row in range(col + 1, n):
            px = remaining.x_output_pauli(col, row)
            if px:
                do("C" + "_XYZ"[px], [col, row])

        # Use the pivot to remove all other terms in the Z observable.
        for row in range(col + 1, n):
            pz = remaining.z_output_pauli(col, row)
            if pz:
                do("XC" + "_XYZ"[pz], [col, row])

        # Fix pauli signs.
        if remaining.z_output(col).sign == -1:
            do("X", [col])
        if remaining.x_output(col).sign == -1:
            do("Z", [col])
    return recorded_circuit


matrix = [
    [0,0,0,0,0,1,1,1,1,1],
    [1,0,0,0,1,0,0,1,1,0],
    [0,1,0,0,1,1,1,1,0,1],
    [0,0,1,0,1,0,1,1,1,1],
    [0,0,0,1,1,1,1,0,0,0],
    [0,0,0,0,1,0,1,1,0,0],
    [0,0,0,0,0,1,0,0,0,0],
    [0,0,0,0,0,0,1,0,0,0],
    [0,0,0,0,0,0,0,1,0,0],
    [0,0,0,0,0,0,0,0,1,0],
]

tableau = bit_matrix_to_tableau(matrix)
print(repr(tableau))

circuit = tableau_to_circuit_simple(tableau)
print(circuit)


def circuit_to_tableau(circuit: stim.Circuit) -> stim.Tableau:
    s = stim.TableauSimulator()
    s.do_circuit(circuit)
    return s.current_inverse_tableau() ** -1


assert circuit_to_tableau(circuit) == tableau
