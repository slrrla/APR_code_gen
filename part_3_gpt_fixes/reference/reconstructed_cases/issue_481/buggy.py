import numpy as np
import qiskit as qk


class Model:
    """
    Minimal reconstruction of the reported model. Each call to modelCircuit
    creates NEW QuantumRegister/ClassicalRegister objects and stores the
    resulting QuantumCircuit as an *instance attribute* (self.circuit).
    Because the registers are freshly created objects every call, and the
    circuit itself is kept as an attribute (never truly released promptly),
    qiskit ends up allocating registers with ever increasing internal ids
    (q0, q7, q140, q273, ...) as reported by the asker.
    """

    def __init__(self, n_quantum=4, n_classic=1, backend='qasm_simulator',
                 shots=1000, seed=42):
        self.n_quantum = n_quantum
        self.n_classic = n_classic
        self.backend = backend
        self.shots = shots
        self.seed = seed
        self.n_model_parameters = (n_quantum + 1) * 1
        self.theta = np.random.uniform(0, 2 * np.pi, self.n_model_parameters)
        self.feature_vector = np.random.uniform(0, 1, n_quantum)
        self.model = self.basicModel

    def basicModel(self):
        """
        scaling with pi to avoid mapping 0 and 1 to the same rotation.
        """
        for i, feature in enumerate(self.feature_vector):
            self.circuit.rx(np.pi * feature, self.quantum_register[i])
            self.circuit.ry(self.theta[i], self.quantum_register[i])
        for qubit in range(self.n_quantum - 1):
            self.circuit.cx(self.quantum_register[qubit], self.quantum_register[qubit + 1])
        self.circuit.ry(self.theta[-1], self.quantum_register[-1])
        self.circuit.measure(self.quantum_register[-1], self.classical_register)

    def modelCircuit(self, printC=False):
        """
        Set up and run the model with the predefined encoders and ansatzes
        for the circuit.
        """
        # BUG: new registers created every call -> qiskit keeps bumping
        # internal register ids, circuit kept alive as self.circuit
        self.quantum_register = qk.QuantumRegister(self.n_quantum)
        self.classical_register = qk.ClassicalRegister(self.n_classic)
        self.circuit = qk.QuantumCircuit(self.quantum_register, self.classical_register)
        self.model()
        job = qk.execute(
            self.circuit,
            backend=qk.Aer.get_backend(self.backend),
            shots=self.shots,
            seed_simulator=self.seed
        )
        results = job.result().get_counts(self.circuit)
        self.model_prediction = results.get('1', 0) / float(self.shots)
        if printC:
            print(self.circuit)
        del (self.circuit)
        return self.model_prediction

    def train(self, target, epochs=5, learning_rate=.1, debug=False):
        from tqdm import tqdm
        mean_loss = np.zeros(epochs)
        accuracy = np.zeros_like(mean_loss)
        n_samples = len(target)
        for epoch in range(epochs):
            acc = 0
            loss = np.ones(n_samples)
            for sample in tqdm(range(n_samples)):
                out = self.modelCircuit()
                acc += np.round(out) == target[sample]
                loss[sample] = abs(out - target[sample])
            accuracy[epoch] = float(acc) / n_samples
            mean_loss[epoch] = np.mean(loss)
            print("mean loss per epoch: ", mean_loss[epoch])
            print("accuracy per epoch: ", accuracy[epoch])
        return self.theta, mean_loss, accuracy


if __name__ == "__main__":
    model = Model()
    target = np.random.randint(0, 2, 10)
    model.train(target, epochs=2)
