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

    def prepare_data(self) -> None:
        """Prepare some template data once and prevent it from being generated repeatedly."""
        if not hasattr(self, "global_data"):
            self.compile_global_data()
        if not hasattr(self, "template"):
            _ = self.get_template()

    def compile_global_data(self) -> None:
        """Prepare a dictionary of global function properties for use in template filling."""
        self.global_data = {'name': self.name}

    def get_template(self) -> code_template.Template:
        """Load function implementation template from file."""
        template_name = f"fbd2py/func/{self.name}.fbdt"
        self.template = code_template.load_template(template_name)
        return self.template

    def compile_section(self, section: str, context: dict, indent=0) -> str:
        """Compile a specific section of this function's template."""
        self.prepare_data()
        sect = self.template.get_section_by_name(section)
        if not sect:
            return ""
        sect_data = context.copy()
        sect_data.update(self.global_data)
        code_template.fill_section(sect, sect_data)
        if indent:
            ret = ""
            for line in sect.content.splitlines():
                ret += int(indent) * " " + line + "\n"
            return ret
        return sect.content

    def compile_sections(self, context: dict) -> dict:
        """Converts the data content of this function into python code."""
        self.prepare_data()
        for sect in self.template.sections:
            self.compile_section(sect.name, context)
        return {sect.name: sect.content for sect in self.template.sections}
