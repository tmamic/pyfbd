"""
@what:  Unit tests for fbd2py.
@why:   QA is important.
@who:   TM
@when:  2022-04-06
"""

# built-in
import unittest

# internal
from pyfbd.fbd2py.pydiagram import PyDiagram

class FBD2PyTests(unittest.TestCase):
    """Compile tests on example diagrams using py2fbd."""

    def test_compile_simple_conn(self):
        sch = PyDiagram.from_file("simple_conn.json")
        sch.compile("simple_conn")

if __name__ == "__main__":
    unittest.main()