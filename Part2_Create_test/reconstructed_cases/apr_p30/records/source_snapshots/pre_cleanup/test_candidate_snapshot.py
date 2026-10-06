import hashlib
from pathlib import Path
import tempfile
import unittest

from adapter import ROOT, snapshot_candidate


class SnapshotTests(unittest.TestCase):
    def test_preserves_each_line_ending_and_unicode_byte_for_byte(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as directory:
            source, target = Path(directory) / "candidate.py", Path(directory) / "snapshot.py"
            for raw in [b"print(1)\n", b"print(1)\r\n", "# 양자\nprint(1)\r\n".encode("utf-8")]:
                source.write_bytes(raw)
                text, present = snapshot_candidate(source, target)
                self.assertTrue(present)
                self.assertEqual(target.read_bytes(), raw)
                self.assertEqual(text, raw.decode("utf-8"))
                self.assertEqual(hashlib.sha256(source.read_bytes()).digest(), hashlib.sha256(target.read_bytes()).digest())

    def test_deleted_candidate_is_explicitly_missing_without_restoring_it(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as directory:
            source, target = Path(directory) / "missing.py", Path(directory) / "snapshot.py"
            text, present = snapshot_candidate(source, target)
            self.assertFalse(present)
            self.assertEqual(text, "")
            self.assertEqual(target.read_bytes(), b"")
            self.assertFalse(source.exists())


if __name__ == "__main__":
    unittest.main()
