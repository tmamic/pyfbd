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
from pyfbd import code_template

class PyDiagram(FBDiagram):

    def make_header(self, template: dict) -> str:
        """Fill in the file header."""
        data = {'source': "spoof",
                'dt': datetime.now(),
                'unique_fbs': len(self._unique_functions),
                'nfbs': len(self.function_blocks),
                'nconn': len(self.connections)}
        return code_template.fill_section(template['header'], data)

    def compile(self, fname: str) -> None:
        """Converts the data content of this diagram into python code."""
        if not fname.endswith(".py"):
            fname += ".py"

        template = code_template.load_template("fbd2py/diagram_template.json")
        with open(fname, "w", encoding="utf-8") as outfile:
            outfile.write(self.make_header(template))