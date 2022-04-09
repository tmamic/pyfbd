"""
@what:  fbd2py extension of generic function block class.
@why:   This class tells the compiler how to write python functions.
@who:   TM
@when:  2022-04-06
"""

# internal
from pyfbd.function import FBDFunc
from pyfbd import code_template

class PyFunc(FBDFunc):

    def get_template(self) -> dict:
        """Load function implementation template from file."""
        template_name = f"fbd2py/{self.name}_template.json"
        return code_template.load_template(template_name)

    def compile(self) -> str:
        """Converts the data content of this function into python code."""
