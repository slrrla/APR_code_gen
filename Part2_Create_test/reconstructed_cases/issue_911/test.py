import ast, contextlib, io, os, runpy, unittest


class T(unittest.TestCase):
    def test_printed_indices_any_format(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            ns = runpy.run_path(os.environ["MUT"])
        lines = out.getvalue().splitlines()
        qc = ns["qc"]
        expected = [list(qc.qubits).index(q) for item in qc.data for q in item[1]]
        self.assertGreater(len(expected), 0)
        actual = None
        try:
            rows = [ast.literal_eval(l.split(":", 1)[1].strip()) for l in lines if l.startswith("qargs :")]
            if rows and all(isinstance(r, list) and all(type(x) is int for x in r) for r in rows):
                actual = [x for r in rows for x in r]
        except (ValueError, SyntaxError):
            pass
        if actual is None:
            actual = [int(l.split(":", 1)[1]) for l in lines if l.startswith("index :")]
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
