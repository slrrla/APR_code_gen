import contextlib, io, os, runpy, unittest
from collections import Counter


class T(unittest.TestCase):
    def test_ghz_outcomes_any_register_layout(self):
        with contextlib.redirect_stdout(io.StringIO()):
            ns = runpy.run_path(os.environ["MUT"])
        self.assertTrue(ns["result"].success)
        merged = Counter()
        for key, n in ns["counts"].items():
            regs = key.split()
            measured = [r for r in regs if set(r) != {"0"}] or [regs[0]]
            merged[measured[0] if len(measured) == 1 else key] += n
        self.assertEqual(sum(merged.values()), 100000)
        self.assertEqual(set(merged), {"000", "111"})
        self.assertAlmostEqual(merged["000"] / 100000, 0.5, delta=0.02)


if __name__ == "__main__":
    unittest.main()
