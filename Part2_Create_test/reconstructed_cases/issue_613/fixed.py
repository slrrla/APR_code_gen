import qiskit
from qiskit import IBMQ
import time
from qiskit import *
from qiskit.tools.visualization import plot_histogram
from qiskit.tools.visualization import plot_bloch_multivector
import matplotlib.pyplot as plt
from qiskit.tools.monitor import job_monitor
from qiskit.transpiler.passes import RemoveBarriers

# IBMQ.save_account('Account key', overwrite=True)  # Run it for once

# 6 bit secret number
secretNumber = '101001'
circuit = QuantumCircuit(6+1, 6)  # 6 qubit for secret no. +1 qubit circuit.
circuit.h([0,1,2,3,4,5])
circuit.x(6)
circuit.h(6)
circuit.barrier()

# splitting the string into char
splitSecretNumber = list(secretNumber)
lengthofSecretNumber = len(splitSecretNumber)
x = 0
while(x < lengthofSecretNumber):
    if(str(splitSecretNumber[x]) == '1'):
        circuit.cx(int(x), 6)
    x = x + 1

circuit.barrier()
circuit.h([0,1,2,3,4,5])
circuit.barrier()
circuit.measure([0,1,2,3,4,5],[0,1,2,3,4,5])
circuit.draw(output="mpl")

IBMQ.load_account()
provider = IBMQ.get_provider('ibm-q')
realMachine = provider.get_backend('ibmq_16_melbourne')

# Remove barriers so the transpiler can optimize across them,
# and use the highest optimization level to reduce depth/gate count.
job = execute(RemoveBarriers()(circuit), realMachine, optimization_level=3, shots=1000)
result = job.result()
counts = result.get_counts()
print(counts)
print(counts.most_frequent())
plot_histogram(counts)
plt.show()
