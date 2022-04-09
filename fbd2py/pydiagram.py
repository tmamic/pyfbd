"""
@what:  fbd2py extension of generic FBD class.
@why:   This class tells the compiler how to convert diagrams to python code.
@who:   TM
@when:  2022-04-06
"""

# built-in
from datetime import datetime

# internal
from pyfbd.diagram import FBDiagram
from pyfbd.fbd2py.pyfunc import PyFunc
from pyfbd import code_template

class PyDiagram(FBDiagram):

    def compile(self, fname: str) -> None:
        """Converts the data content of this diagram into python code."""
        if not fname.endswith(".py"):
            fname += ".py"

        template = code_template.load_template("fbd2py/diagram.fbdt")
        with open(fname, "w", encoding="utf-8") as outfile:
            return