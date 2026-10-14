"""Report actual bit locations through public APIs, independently of formatting.

The original example is also probed with nonzero bits and a leading register:
hardcoded zeroes, unrelated register objects and circuit/local-index confusion
must fail. Both register/local output and circuit-plus-register output are valid.
"""
import os
from pathlib import Path
import sys
import unittest

CASE_DIR = Path(__file__).resolve().parent
MUT = os.environ.get("MUT", str(CASE_DIR / "fixed.py"))

sys.path.insert(0, str(CASE_DIR.parent))
from bit_location_oracle import check_bit_reporting

class TestIntent(unittest.TestCase):
    def test_public_bit_locations(self):
        for h_index, control_index, prefix_size in ((0,0,0), (1,1,0), (1,0,0), (1,0,1)):
            with self.subTest(h_index=h_index, control_index=control_index, prefix_size=prefix_size):
                check_bit_reporting(MUT, h_index=h_index, control_index=control_index, prefix_size=prefix_size)

if __name__ == "__main__":
    unittest.main()
