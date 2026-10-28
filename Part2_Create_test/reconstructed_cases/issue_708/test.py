# intent: Preserve the UTC offset when interpreting the backend-properties timestamp.
# bug_type: WRONG_OUTPUT
import contextlib
import io
import os
import runpy
import unittest

CASE_DIR = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("MUT", os.path.join(CASE_DIR, "fixed.py"))

from datetime import datetime, timezone, timedelta

class Test(unittest.TestCase):
    def test_utc_timestamp(self):
        with contextlib.redirect_stdout(io.StringIO()):
            ns = runpy.run_path(MUT)
        actual = ns['last_update_time']
        self.assertIsInstance(actual, datetime)
        self.assertIsNotNone(actual.tzinfo, 'The supplied +00:00 offset must not be discarded.')
        self.assertEqual(actual.utcoffset(), timedelta(0))
        self.assertEqual(actual, datetime(2019,11,11,7,16,13,tzinfo=timezone.utc))

if __name__ == "__main__":
    unittest.main(argv=[""])
