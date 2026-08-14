# The answer clarifies that qiskit.compiler.transpile() uses
# qiskit.tools.parallel.parallel_map() under the hood, which in turn
# uses concurrent.futures.ProcessPoolExecutor / the multiprocessing
# module to run transpile() on each circuit in a separate process,
# but only by default on Linux (Python < 3.9) or macOS (Python < 3.8).
# On other platforms/versions it falls back to sequential execution
# unless explicitly configured otherwise.
from qiskit import QuantumCircuit
from qiskit.compiler import transpile
from qiskit.tools import parallel_map  # the underlying mechanism used by transpile()

qc1 = QuantumCircuit(2)
qc1.h(0)
qc1.cx(0, 1)

qc2 = QuantumCircuit(2)
qc2.x(0)
qc2.cx(0, 1)

circuits = [qc1, qc2]

# transpile() internally calls parallel_map(), which relies on
# concurrent.futures.ProcessPoolExecutor (backed by multiprocessing)
# to transpile each circuit in a separate process when parallel
# execution is available and enabled.
transpiled = transpile(circuits)

# Parallelism can be controlled explicitly, e.g. via:
# from qiskit import user_config
# user_config.set_config('parallel', 'True')
# or by setting the QISKIT_IN_PARALLEL / QISKIT_NUM_PROCS environment variables.
