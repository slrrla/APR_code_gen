import numpy as np
import qiskit as qk


class Model:
    """
    Fixed version: registers removed entirely (registerless circuit built
    fresh from integers each call), and the circuit is a local variable
    returned from self.model()/modelCircuit() rather than an attribute kept
    alive on self. This avoids qiskit's internal register-id counter from
    growing without bound and lets the garbage collector clean up circuits
    promptly between iterations.
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
        Registerless circuit: qubits/clbits addressed by plain integers.
        """
        circuit = qk.QuantumCircuit(self.n_quantum, self.n_classic)
        for i, feature in enumerate(self.feature_vector):
            circuit.rx(np.pi * feature, i)
            circuit.ry(self.theta[i], i)
        for qubit in range(self.n_quantum - 1):
            circuit.cx(qubit, qubit + 1)
        circuit.ry(self.theta[-1], -1)
        circuit.measure(-1, 0)
        return circuit

    def modelCircuit(self, printC=False):
        """
        Set up and run the model with the predefined encoders and ansatzes
        for the circuit. Circuit is local -- no growing register ids, no
        dangling references kept on self.
        """
        circuit = self.model()
        job = qk.execute(
            circuit,
            backend=qk.Aer.get_backend(self.backend),
            shots=self.shots,
            seed_simulator=self.seed
        )
        results = job.result().get_counts(circuit)
        counts = 0
        for key, value in results.items():
            if key == '1':
                counts += value
        self.model_prediction = counts / float(self.shots)
        if printC:
            print(circuit)
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
