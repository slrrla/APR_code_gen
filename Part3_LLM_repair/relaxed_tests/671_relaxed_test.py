import contextlib, io, os, runpy, unittest


class T(unittest.TestCase):
    def test_registers_only(self):
        with contextlib.redirect_stdout(io.StringIO()):
            ns = runpy.run_path(os.environ["MUT"])
        c = ns["c"]
        self.assertEqual((c.num_qubits, c.num_clbits), (9, 1))
        self.assertEqual(c.qregs, [ns["a"]] + ns["v"])
        self.assertEqual(c.cregs, [ns["b"]])
        self.assertEqual(c.qubits, list(ns["a"]) + [q for r in ns["v"] for q in r])


if __name__ == "__main__":
    unittest.main()
