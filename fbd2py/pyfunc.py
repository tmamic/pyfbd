"""
@what:  fbd2py extension of generic function block class.
@why:   This class tells the compiler how to write python functions.
@who:   TM
@when:  2022-04-06
"""

# internal
from pyfbd.function import FBDFunc

class PyFunc(FBDFunc):

    def compile(self) -> str:
        """Converts the data content of this function into python code."""
        lines = [f"def {self.name}():",
                 "    pass"]
        return lines