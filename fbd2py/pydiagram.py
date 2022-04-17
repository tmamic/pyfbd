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

    def transform_objects(self) -> None:
        """Transforms generic objects into their PyDiagram versions."""
        for fname, func in self._unique_functions.items():
            self._unique_functions[fname] = PyFunc.load(func.dump())

    def make_fb_links(self, template: code_template.Template) -> dict:
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

    def make_typedefs(self) -> str:
        """Collect typedef outptus of functions."""
        # gather function outputs for typedefs
        typedef_out = ""
        for _, func in self._unique_functions.items():
            output = func.compile_section("type_defs", {})
            typedef_out += output
        return typedef_out

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

        global_data["type_defs"] = self.make_typedefs()

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