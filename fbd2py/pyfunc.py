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

    def add_output_def(self, out: list) -> None:
        """Appends the definition of function outputs to given out list."""
        outputs = list(self.outputs.keys())
        if not outputs:
            out.append(f"    ret = None")
            return

        cur = outputs.pop(0)
        out.append(f"    ret = {{'{cur}': None")
        while outputs:
            cur = outputs.pop(0)
            out.append(f"           '{cur}': None")
        out[-1] += "}"

    def get_template(self) -> dict:
        """Load function implementation template from file."""
        template_name = f"fbd2py/{self.name}_template.json"
        return code_template.load_template(template_name)

    def compile(self) -> str:
        """Converts the data content of this function into python code."""
        args = ["cls"]
        if self.inputs:
            args.append("inputs")
        if self.state:
            args.append("state")
        lines = [f"def {self.name}({', '.join(args)}):"]

        template = self.get_template()
        for line in code_template.fill_section(template['docstring'], {}):
            lines.append(f"    {line}")

        self.add_output_def(lines)

        for line in code_template.fill_section(template['body'], {}):
            lines.append(f"    {line}")

        lines.append("    return ret")

        return lines