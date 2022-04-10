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
        global_data = {'source': fname,
                       'diagtemplate': template.fname,
                       'schname': self.schname if hasattr(self, "schname") else "unnamed",
                       'dt': datetime.now(),
                       'unique_fbs': len(self._unique_functions),
                       'nfbs': len(self.function_blocks),
                       'nconn': len(self.connections)}

        for sect in template.sections:
            code_template.fill_section(sect, global_data)
            print(f"{sect.name}:\n---\n{sect.content}")

        with open(fname, "w", encoding="utf-8") as outfile:
            for sect in template.sections:
                filler = "." * (50 - len(sect.name))
                print(f"[INFO] Writing {sect.name}{filler}", end="")
                if sect.complete:
                    outfile.write(sect.content)
                    print(f" OK")
                else:
                    print(f" INCOMPLETE")