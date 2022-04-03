"""
@what:  Unit tests for variable class.
@why:   QA is important.
@who:   TM
@when:  2022-03-04
"""

# built-in
import unittest

# internal
from pyfbd.variable import FBDVar

class VariableTests(unittest.TestCase):
    """All unit tests for variable.py should be contained here."""

    def test_dump_and_load(self):
        var = FBDVar("tstvar", "dtype")
        img = FBDVar.load(var.dump())
        self.assertEqual(var.name, img.name)
        self.assertEqual(var.type, img.type)

if __name__ == "__main__":
    unittest.main()