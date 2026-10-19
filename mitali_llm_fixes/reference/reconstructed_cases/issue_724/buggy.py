from qiskit.circuit import QuantumCircuit, ParameterVector
from qiskit import BasicAer, execute

n = 58
p = ParameterVector('p', n)
sum = [0 for _ in range(n)]

ATCQNN_CIRCUIT = QuantumCircuit(4, 4)
for i in range(4):
    ATCQNN_CIRCUIT.rx(p[i], i)

# my code is in here such like
# for i in range(n):
#     ATCQNN_CIRCUIT.rx(p[i], i)

# Bug: bind_parameters returns a copy by default, but the result is discarded,
# so ATCQNN_CIRCUIT still has unbound parameters.
ATCQNN_CIRCUIT.bind_parameters({p: sum})
# instead of the above line, I tried also this below one...
# ATCQNN_CIRCUIT.bind_parameters({p[i]: sum[i] for i in range(58)})

ATCQNN_CIRCUIT.barrier()
ATCQNN_CIRCUIT.measure(range(4), range(4))
print(ATCQNN_CIRCUIT.num_parameters)

backend = BasicAer.get_backend('qasm_simulator')
results = execute(ATCQNN_CIRCUIT, backend).result()
a = results.get_counts(ATCQNN_CIRCUIT)
print(a)
