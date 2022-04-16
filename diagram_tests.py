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
        var1 = FBDVar("tstvar", "dtype")
        var2 = FBDVar("not_tstvar", "dtype")
        func1 = FBDFunc("tstfunc", (var1,), (var2,), tuple())
        func2 = FBDFunc("tstfunc", (var1,), (var2,), tuple())
        f1ref = diagram.add_function(func1)
        f2ref = diagram.add_function(func2)
        diagram.add_connection(f"{f1ref}.not_tstvar", f"{f2ref}.tstvar")
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
        f1 = FBDFunc("tstf1", (var1,), (var2,), tuple())
        f2 = FBDFunc("tstf1", (var2,), (var2,), tuple())

        _ = sch1.add_function(f1)
        _ = sch2.add_function(f1)
        self.assertEqual(sch1, sch2)

        _ = sch1.add_function(f2)
        self.assertNotEqual(sch1, sch2)

        _ = sch2.add_function(f2)
        self.assertEqual(sch1, sch2)

        _ = sch1.add_function(f1)
        _ = sch2.add_function(f2)
        self.assertNotEqual(sch1, sch2)

        # check that modules are no longer equal if their connection matrices differ
        sch_a = FBDiagram.from_file("simple_conn.json")
        sch_b = FBDiagram.from_file("simple_conn.json")
        self.assertEqual(sch_a, sch_b)

        sch_b.add_connection("obj[1].X", "obj[0].A")
        self.assertNotEqual(sch_a, sch_b)

    def test_uid(self):
        diagram = FBDiagram()
        func = FBDFunc("tstfunc", tuple(), tuple(), tuple())

        # confirm that different instances of the same function get different IDs
        uid1 = diagram.add_function(func)
        uid2 = diagram.add_function(func)
        self.assertNotEqual(uid1, uid2)

    def test_save_and_load_from_file(self):
        sch = FBDiagram()
        var = FBDVar("tstvar", "dtype")
        func = FBDFunc("tstfunc", (var,), (var,), (var,))
        _ = sch.add_function(func)
        sch.save("test_scheme.json")
        img = FBDiagram.from_file("test_scheme.json")
        self.assertEqual(sch, img)

if __name__ == "__main__":
    unittest.main()