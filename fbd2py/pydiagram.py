"""
@what:  fbd2py extension of generic FBD class.
@why:   This class tells the compiler how to convert diagrams to python code.
@who:   TM
@when:  2022-04-06
"""

# internal
from pyfbd.diagram import FBDiagram

class PyDiagram(FBDiagram):

    def compile(self, fname: str) -> None:
        """Converts the data content of this diagram into python code."""
        if not fname.endswith(".py"):
            fname += ".py"

        content = ""
        with open(fname, "w", encoding="utf-8") as outfile:
            outfile.write(content)