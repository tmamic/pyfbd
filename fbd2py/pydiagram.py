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
from pyfbd.code_template import Template

class PyDiagram(FBDiagram):

    UNIQUE_SECTS = ("type_defs", "func_def")
    INSTANCE_SECTS = ("state_def", "func_call")

    def transform_objects(self) -> None:
        """Transforms generic objects into their PyDiagram versions."""
        for fname, func in self._unique_functions.items():
            self._unique_functions[fname] = PyFunc.load(func.dump())

    def make_fb_links(self, template: Template) -> dict:
        """
        Create a dictionary of variable assignments which matches the data flow specified
        by connection matrix.
        """
        print("[INFO] Linking function blocks...")
        ret = {"free_in": [], "free_out": [], "def_in": [], "def_out": []}

        # make a list of all inputs and outputs in the diagram
        for uid, fname in self.function_blocks.items():
            for fbin in self._unique_functions[fname].inputs:
                ret['free_in'].append(f"{uid}.{fbin}")
            for fbout in self._unique_functions[fname].outputs:
                ret['free_out'].append(f"{uid}.{fbout}")

        for src, dst in self.connections.items():
            # for now we completely disrespect the data flow!!!
            if src in ret['free_out']:
                if dst in ret['free_in']:
                    ret['free_in'].remove(dst)
                    ret['free_out'].remove(src)
                    ret["def_in"].append(dst)
                    ret["def_out"].append(src)
                    print(f"       {src} --> {dst}")
                else:
                    print(f"[ERROR] Target '{dst}' is not an input.")
            else:
                print(f"[ERROR] Source '{src}' is not an output.")

        print(f"[INFO] Done.")
        if ret['free_in']:
            print(f"[INFO] Free inputs: {ret['free_in']}")
        if ret['free_out']:
            print(f"[INFO] Free outputs: {ret['free_out']}")
        return ret

    def fill_input_section(self, template:Template,  sect: str, contributors) -> None:
        """Locate input section from template and fill it from contributors' output sections."""
        in_section = template.get_section_by_name(sect)
        if in_section.type != "in":
            raise ValueError("Supplied section name does not point to input section.")

        ret = ""
        indent = in_section.properties['indent'] if 'indent' in in_section.properties else 0
        for func in contributors:
            ret += func.compile_section(sect, {}, indent)
        if ret:
            in_section.content = ret
            in_section.complete = True

    def compile(self, fname: str) -> None:
        """Converts the data content of this diagram into python code."""
        # specialize objects for PyFBD
        self.transform_objects()

        if not fname.endswith(".py"):
            fname += ".py"

        template = code_template.load_template("fbd2py/diagram.fbdt")

        conns = self.make_fb_links(template)

        global_data = {'source': fname,
                       'diagtemplate': template.fname,
                       'schname': self.schname if hasattr(self, "schname") else "unnamed",
                       'dt': datetime.now(),
                       'unique_fbs': len(self._unique_functions),
                       'nfbs': len(self.function_blocks),
                       'nconn': len(self.connections)}

        # fill in sections to which unique functions contribute
        for sect_name in self.UNIQUE_SECTS:
            unq = (func for _, func in self._unique_functions.items())
            self.fill_input_section(template, sect_name, unq)
            global_data[sect_name] = template.get_section_by_name(sect_name).content

        # fill in sections where each fb instance contributes
        for sect_name in self.INSTANCE_SECTS:
            fnames = (fname for _, fname in self.function_blocks.items())
            ins = (self._unique_functions[fname] for fname in fnames)
            self.fill_input_section(template, sect_name, ins)
            global_data[sect_name] = template.get_section_by_name(sect_name).content

        for sect in template.sections:
            code_template.fill_section(sect, global_data)

        with open(fname, "w", encoding="utf-8") as outfile:
            for sect in template.sections:
                filler = "." * (50 - len(sect.name))
                print(f"[INFO] Writing {sect.name}{filler}", end="")
                if sect.complete:
                    outfile.write(sect.content)
                    print(f" OK")
                else:
                    print(f" INCOMPLETE")