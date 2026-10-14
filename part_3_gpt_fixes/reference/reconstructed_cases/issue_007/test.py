# intent: serialise a Result via res.to_dict() (a dict/str), then rebuild it with Result.from_dict(eval(line)) so counts survive the round trip
# bug_type: CRASH
import os, runpy, tempfile, unittest

from qiskit.result import Result

CASE_DIR = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("MUT", os.path.join(CASE_DIR, "fixed.py"))

EXPECTED_COUNTS = {"00": 512, "11": 512}


def _run(path):
    cwd = os.getcwd()
    tmp = tempfile.mkdtemp()
    try:
        os.chdir(tmp)
        ns = runpy.run_path(path)  # buggy version raises here -> test fails (bug found)
        written = None
        fname = os.path.join(tmp, "result.txt")
        if os.path.exists(fname):
            with open(fname) as f:
                written = f.read()
        return ns, written
    finally:
        os.chdir(cwd)


class Test(unittest.TestCase):
    def test_roundtrip_counts(self):
        ns, written = _run(MUT)

        results = [v for v in ns.values() if isinstance(v, Result)]
        self.assertTrue(results, "no Result object produced by the script")

        restored = ns.get("restored")
        self.assertIsInstance(restored, Result, "script must rebuild a Result object")

        # INTENT: the serialised/deserialised Result carries the same counts
        counts = dict(restored.get_counts())
        self.assertEqual(counts, EXPECTED_COUNTS)

        self.assertEqual(restored.backend_name, "ibmq_16_melbourne")
        self.assertEqual(restored.backend_version, "1.1.0")
        self.assertTrue(restored.success)

        # the on-disk representation must be text that can be evaluated back to a dict
        self.assertIsNotNone(written, "script must write the serialised result to result.txt")
        self.assertIsInstance(written, str)
        import ast

        payload = ast.literal_eval(written)
        self.assertIsInstance(payload, dict)
        self.assertEqual(payload["backend_name"], "ibmq_16_melbourne")
        self.assertEqual(
            dict(Result.from_dict(payload).get_counts()), EXPECTED_COUNTS
        )


if __name__ == "__main__":
    unittest.main(argv=[""])
