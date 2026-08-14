# The `hello_qiskit` helper module is just a thin wrapper around
# qiskit_textbook.games.hello_quantum with a local `exercises` list.
# Instead of relying on a missing `hello_qiskit.py` file, define the
# equivalent functionality directly using qiskit_textbook.

from qiskit_textbook.games import hello_quantum

exercises = [
    {
        'initialize': [],
        'success_condition': {},
        'allowed_gates': {'0': {'x': 3}, '1': {}, 'both': {}},
        'vi': [[1], True, False],
        'mode': 'line',
        'qubit_names': {'0': 'q[0]', '1': 'q[1]'}
    }
]

def run_puzzle(j):
    puzzle = hello_quantum.run_game(
        exercises[j]['initialize'],
        exercises[j]['success_condition'],
        exercises[j]['allowed_gates'],
        exercises[j]['vi'],
        qubit_names=exercises[j]['qubit_names'],
        mode=exercises[j]['mode']
    )
    return puzzle

result = run_puzzle(0)
print(result)
