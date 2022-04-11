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

        input_sections = {sect.name: "" for sect in template.iter_sections_by_type("in")}
        for func in self._unique_functions:
            pyfunc_obj = PyFunc.load(func.dump())
            function_outs = pyfunc_obj.compile_sections()
            print(f"[INFO] Compiling outputs for {func.name}.")
            for sect_name, content in function_outs.items():
                section = template.get_section_by_name(sect_name)
                indent = 0
                if 'indent' in section.properties:
                    indent = int(section.properties['indent'])
                if sect_name in input_sections:
                    for line in content.splitlines():
                        indented = (" " * indent + line) + "\n"
                        section.content += indented
                        input_sections[sect_name] += indented

        for sect, content in input_sections.items():
            if not content:
                print(f"[INFO] Section {sect} empty.")
        for sect in template.sections:
            code_template.fill_section(sect, input_sections)

        with open(fname, "w", encoding="utf-8") as outfile:
            for sect in template.sections:
                filler = "." * (50 - len(sect.name))
                print(f"[INFO] Writing {sect.name}{filler}", end="")
                if sect.complete:
                    outfile.write(sect.content)
                    print(f" OK")
                else:
                    print(f" INCOMPLETE")