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

        # confirm that base data content is intact
        for item in FBDVar.DATAMODEL:
            self.assertEqual(var.__dict__[item], img.__dict__[item])

        # ensure that var and image are equal, but not the same object
        self.assertEqual(var, img)
        self.assertIsNot(var, img)

        # ensure that different variables are not seen as equal
        self.assertNotEqual(var, FBDVar("not tstvar", "dtype"))
        self.assertNotEqual(var, FBDVar("tstvar", "not dtype"))

if __name__ == "__main__":
    unittest.main()