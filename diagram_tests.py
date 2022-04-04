"""
@what:  Unit tests for diagram class.
@why:   QA is important.
@who:   TM
@when:  2022-04-04
"""

# built-in
import unittest

# internal
from pyfbd.diagram import FBDiagram
from pyfbd.function import FBDFunc

class DiagramTests(unittest.TestCase):
    """All unit tests for function.py should be contained here."""

    def test_dump_and_load(self):
        diagram = FBDiagram()
        img = FBDiagram.load(diagram.dump())

        # ensure object equivalence, but not identity
        self.assertIsNot(diagram, img)
        self.assertEqual(diagram, img)

    def test_uid(self):
        diagram = FBDiagram()
        func = FBDFunc("tstfunc", tuple(), tuple(), tuple())

        # confirm that different instances of the same function get different IDs
        uid1 = diagram.add_function(func)
        uid2 = diagram.add_function(func)
        self.assertNotEqual(uid1, uid2)

if __name__ == "__main__":
    unittest.main()