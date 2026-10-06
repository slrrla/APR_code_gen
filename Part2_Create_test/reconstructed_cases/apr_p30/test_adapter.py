"""Contract checks for task selection, answer exclusion and independent validation."""
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

import adapter


class AdapterContracts(unittest.TestCase):
    def test_interrupted_prepare_cannot_overwrite_existing_repair(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp) / "interrupted_run"
            candidate = directory / "tasks/issue_001/workspace/buggy.py"
            candidate.parent.mkdir(parents=True)
            candidate.write_text("existing completed repair", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "nonempty run directory"):
                adapter.prepare(directory, archive=None)
            self.assertEqual(candidate.read_text(encoding="utf-8"), "existing completed repair")

    def test_unittest_exit_zero_does_not_mean_test_pass(self):
        self.assertEqual(adapter.classify_run(0, "hello", "")[0], "INVALID_RUN")
        self.assertEqual(adapter.classify_run(0, "", "Ran 0 tests in 0s\n\nOK\n")[0], "INVALID_RUN")
        self.assertEqual(adapter.classify_run(0, "", "Ran 2 tests in 0s\n\nOK (skipped=1)\n")[0], "INVALID_RUN")
        self.assertEqual(adapter.classify_run(0, "", "Ran 2 tests in 0s\n\nOK\n"), ("PASS", 2, 0))

    def test_answer_material_is_not_repair_context(self):
        text = "Title:\nA question\nCategory:\nSECRET CATEGORY ANSWER\nQuestion:\nHow does this work?\nOriginal buggy code:\ncode\nSolution explanation:\nSECRET FIX\nOriginal fixed code:\nREFERENCE"
        title, question = adapter.question_context(text)
        self.assertEqual(title, "A question")
        self.assertEqual(question, "How does this work?")
        self.assertNotIn("SECRET", question)
        self.assertEqual(adapter.question_context("No structured question")[1], "")

    def test_selection_requires_thirty_and_uses_current_repair_evidence(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            cases, records = [], []
            for i in range(1, 32):
                name = f"issue_{i:03}"
                directory = root / name
                directory.mkdir()
                for filename in ["buggy.py", "fixed.py", "test.py", "original_question.txt"]:
                    (directory / filename).write_text(filename, encoding="utf-8")
                cases.append({"case": name, "row": i, "validity": "p"})
                records.append({"case": name, "version": "0.9.0", "variant": "fixed", "status": "PASS", "tests_run": 1,
                                "command": [sys.executable], "source_sha256": adapter.sha(directory / "fixed.py"),
                                "test_sha256": adapter.sha(directory / "test.py")})
            override = dict(records[0], version="0.10.0", evidence_source="repair01/results.json")
            merged = adapter.merge_evidence(records, [override])
            selected, exclusions = adapter.select_cases({"cases": cases}, merged, root)
            self.assertEqual(len(selected), 30)
            self.assertEqual(selected[0]["version"], "0.10.0")
            self.assertEqual(selected[-1]["case"], "issue_030")
            self.assertTrue(any(x["case"] == "issue_031" for x in exclusions))
            with self.assertRaises(ValueError):
                adapter.select_cases({"cases": cases[:29]}, records, root)
            with self.assertRaises(ValueError):
                adapter.select_cases({"cases": cases}, records, root, 29)

    def test_candidate_runs_through_separate_test_with_mut(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            source = directory / "candidate.py"
            source.write_text("answer = 42\n", encoding="utf-8")
            test = directory / "test.py"
            test.write_text("import os,runpy,unittest\nclass Test(unittest.TestCase):\n def test_intent(self):\n  self.assertEqual(runpy.run_path(os.environ['MUT'])['answer'],42)\nif __name__ == '__main__': unittest.main()\n", encoding="utf-8")
            task = {"case": "issue_001", "version": "0.1.0", "interpreter": sys.executable}
            result = adapter.execute_test(task, source, test, "candidate", directory, 15)
            self.assertEqual(result["status"], "PASS")
            self.assertEqual(result["tests_run"], 1)
            self.assertEqual(result["test_sha256"], adapter.sha(test))
            self.assertTrue(Path(result["runtime_dir"]).is_relative_to(directory))
            source.write_text("answer = 13\n", encoding="utf-8")
            result = adapter.execute_test(task, source, test, "bad_candidate", directory, 15)
            self.assertEqual(result["status"], "FAIL")

    def test_child_process_cannot_inherit_model_credentials(self):
        with tempfile.TemporaryDirectory() as temp:
            work = Path(temp)
            os.environ["APR_TEST_SECRET"] = "secret"
            try:
                environment = adapter.runtime_environment(Path(sys.executable), work, work / "candidate.py", None)
                self.assertNotIn("APR_TEST_SECRET", environment)
                self.assertEqual(environment["HOME"], str(work))
            finally:
                del os.environ["APR_TEST_SECRET"]

    def test_suspicious_error_hiding_and_no_change_are_reported(self):
        original = "answer = 42\nprint(answer)\n"
        self.assertFalse(adapter.patch_audit(original, original)["changed"])
        hidden = "try:\n answer = 42\nexcept Exception:\n pass\n"
        self.assertTrue(adapter.patch_audit(original, hidden)["adds_broad_except"])
        self.assertFalse(adapter.patch_audit(original, "def broken(")["syntax_ok"])

    def test_changed_validator_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            source = directory / "source"
            source.mkdir()
            (directory / "validator").mkdir()
            for filename in ["buggy.py", "fixed.py", "test.py", "original_question.txt"]:
                (source / filename).write_text(filename, encoding="utf-8")
            (directory / "original.py").write_bytes((source / "buggy.py").read_bytes())
            (directory / "validator/test.py").write_bytes((source / "test.py").read_bytes())
            task = {"case": "issue_001", "source_dir": str(source),
                    "hashes": {p.name: adapter.sha(p) for p in source.iterdir()}}
            adapter.check_immutable(task, directory)
            (directory / "validator/test.py").write_text("modified", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Immutable validator"):
                adapter.check_immutable(task, directory)


if __name__ == "__main__":
    unittest.main()
