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

    def get_template(self) -> code_template.Template:
        """Load function implementation template from file."""
        template_name = f"fbd2py/{self.name}_template.fbdt"
        return code_template.load_template(template_name)

    def compile_sections(self) -> dict:
        """Converts the data content of this function into python code."""
        template = self.get_template()
        func_data = {'name': self.name}
        for sect in template.sections:
            code_template.fill_section(sect, func_data)

        return {sect.name: sect.content for sect in template.sections}
