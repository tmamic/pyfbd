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

class DiagramTests(unittest.TestCase):
    """All unit tests for function.py should be contained here."""

    def test_dump_and_load(self):
        diagram = FBDiagram()
        img = FBDiagram.load(diagram.dump())

        # ensure object equivalence, but not identity
        self.assertIsNot(diagram, img)
        self.assertEqual(diagram, img)

if __name__ == "__main__":
    unittest.main()