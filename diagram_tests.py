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
from pyfbd.variable import FBDVar

class DiagramTests(unittest.TestCase):
    """All unit tests for function.py should be contained here."""

    def test_dump_and_load(self):
        diagram = FBDiagram()
        func = FBDFunc("tstfunc", tuple(), tuple(), tuple())
        _ = diagram.add_function(func)
        img = FBDiagram.load(diagram.store())

        # ensure object equivalence, but not identity
        self.assertIsNot(diagram, img)
        self.assertEqual(diagram, img)

    def test_topological_equivalence(self):
        # make sure that diagrams with different functions are not equivalent
        sch1 = FBDiagram()
        sch2 = FBDiagram()
        var1 = FBDVar("tstvar", "dtype")
        var2 = FBDVar("not tstvar", "dtype")
        f1 = FBDFunc("tstf1", (var1,), tuple(), tuple())
        f2 = FBDFunc("tstf1", (var2,), tuple(), tuple())

        _ = sch1.add_function(f1)
        _ = sch2.add_function(f1)
        self.assertEqual(sch1, sch2)

        _ = sch1.add_function(f2)
        self.assertNotEqual(sch1, sch2)

    def test_uid(self):
        diagram = FBDiagram()
        func = FBDFunc("tstfunc", tuple(), tuple(), tuple())

        # confirm that different instances of the same function get different IDs
        uid1 = diagram.add_function(func)
        uid2 = diagram.add_function(func)
        self.assertNotEqual(uid1, uid2)

if __name__ == "__main__":
    unittest.main()