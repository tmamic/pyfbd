"""
@what:  Unit tests for diagram class.
@why:   QA is important.
@who:   TM
@when:  2022-04-04
"""

# built-in
import unittest

from numpy import diag

# internal
from pyfbd.diagram import FBDiagram

class DiagramTests(unittest.TestCase):
    """All unit tests for function.py should be contained here."""

    def test_dump_and_load(self):
        diagram = FBDiagram()
        img = FBDiagram.load(diagram.dump())

if __name__ == "__main__":
    unittest.main()