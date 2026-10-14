import sys
sys.path.append("../../")

from qiskit import QuantumProgram

#visualization
from tools.visualization import plot_histogram

#set up registers
qp = QuantumProgram()
q = qp.create_quantum_register("q", 3)
c = qp.create_classical_register("c", 3)

#define our circuit
threeQ = qp.create_circuit("threeQ", [q], [c])
threeQ.measure(q[0], c[0])
threeQ.measure(q[1], c[1])
threeQ.measure(q[2], c[2])

#run
result = qp.execute(["threeQ"])

#plot
plot_histogram(result.get_counts("threeQ"))
