"""
@what:  Unit tests for function class.
@why:   QA is important.
@who:   TM
@when:  2022-03-04
"""

# built-in
import unittest

# internal
from pyfbd.function import FBDFunc
from pyfbd.variable import FBDVar

class FunctionTests(unittest.TestCase):
    """All unit tests for function.py should be contained here."""

    def test_dump_and_load(self):
        tstin = (FBDVar("X", "ttype"), FBDVar("Y", "ttype"))
        tststate = (FBDVar("S", "ttype"),)
        tstout = (FBDVar("O", "ttype"),)
        func = FBDFunc("tstfunc", tstin, tstout, tststate)
        img = FBDFunc.load(func.dump())

        # ensure object equivalence, but not identity
        self.assertIsNot(func, img)
        self.assertEqual(func, img)

        # ensure invalid var name fails
        with self.assertRaises(KeyError):
            img.get_input_var("S")

if __name__ == "__main__":
    unittest.main()