import contextlib, io, os, runpy, unittest


class T(unittest.TestCase):
    def test_parsed_circuit_was_executed(self):
        with contextlib.redirect_stdout(io.StringIO()):
            ns = runpy.run_path(os.environ["MUT"])
        result = ns["result"]
        self.assertTrue(result.success)
        self.assertEqual(len(result.results), 1)
        header = result.results[0].header
        header = header.to_dict() if hasattr(header, "to_dict") else dict(header)
        self.assertEqual(header.get("n_qubits"), 2)
        self.assertEqual(header.get("memory_slots"), 2)


if __name__ == "__main__":
    unittest.main()
