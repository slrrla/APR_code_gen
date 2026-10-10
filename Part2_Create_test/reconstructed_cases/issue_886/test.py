import contextlib, io, os, runpy, unittest


class T(unittest.TestCase):
    def test_job_runs_and_control_zero_keeps_target_zero(self):
        with contextlib.redirect_stdout(io.StringIO()):
            ns = runpy.run_path(os.environ["MUT"])
        result = ns["job"].result()
        self.assertTrue(result.success)
        counts = result.get_counts()
        self.assertEqual(sum(counts.values()), 1024)
        self.assertTrue(all(set(k.replace(" ", "")) == {"0"} for k in counts), counts)


if __name__ == "__main__":
    unittest.main()
