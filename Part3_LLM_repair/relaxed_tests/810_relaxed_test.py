import contextlib, io, os, runpy, unittest


class T(unittest.TestCase):
    def test_raw_counts_any_variable_name_and_shots(self):
        with contextlib.redirect_stdout(io.StringIO()):
            ns = runpy.run_path(os.environ["MUT"])
        dicts = [v for k, v in ns.items() if not k.startswith("__") and isinstance(v, dict) and v and set(v) <= {"0", "1"}]
        self.assertTrue(dicts, "no raw counts dictionary")
        counts = dicts[0]
        result = ns["job"].result()
        shots = result.results[0].shots
        self.assertTrue(result.success)
        self.assertEqual(sum(counts.values()), shots)
        self.assertEqual(set(counts), {"0", "1"})
        self.assertLess(abs(counts["1"] / shots - .5), .3)
        self.assertEqual(counts, result.get_counts())


if __name__ == "__main__":
    unittest.main()
