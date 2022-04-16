"""
@what:  Container object for function block diagrams.
@why:   This is the object that we want to build in the end.
@who:   TM
@when:  2022-04-04
"""

# built-in
import json
import re

# internal
from pyfbd.fbdobj import FBDObj
from pyfbd.function import FBDFunc

VAR_REF_REGEX = re.compile(r"(.*)\.(.*)")
def _parse_var_ref(ref: str) -> "tuple[str]":
    """Utility function. Parses <func>.<var> into separate tags."""
    res = re.findall(VAR_REF_REGEX, ref)
    if len(res) == 1:
        return res[0]
    return ValueError(f"Could not parse reference {ref}.")

class FBDiagram(FBDObj):
    """Data model of an FBD containing multiple functions and their interconnections."""
    DATAMODEL = ("connections",)
    METADATA = ("_cid", "schname")

    def __init__(self) -> None:
        self._cid = 0
        self._unique_functions = {}
        self.function_blocks = {}
        self.connections = {}

    def dump(self) -> dict:
        """Convert diagram data to dictionary."""
        ret = {key: self.__dict__[key] for key in FBDiagram.DATAMODEL}
        ret['func_ifaces'] = {name: func.dump() for name, func in self._unique_functions.items()}
        ret['func_blocks'] = {uid: fname for uid, fname in self.function_blocks.items()}
        return ret

    def store(self) -> dict:
        """Store object with added metadata to dictionary. Prefered when saving state of instance."""
        ret = self.dump()
        for key in FBDiagram.METADATA:
            if key in self.__dict__:
                ret.update({key: self.__dict__[key]})
        return ret

    @classmethod
    def load(cls, data: dict) -> "FBDiagram":
        """Construct diagram object from data."""
        ret = cls()
        for key in cls.DATAMODEL:
            # we are okay with keyerror here - datamodel must be complete
            ret.__dict__[key] = data[key]
        for key in cls.METADATA:
            # we are fine with metadata missing
            if key in data:
                ret.__dict__[key] = data[key]
        for name, fdump in data['func_ifaces'].items():
            func = FBDFunc.load(fdump)
            ret._unique_functions[name] = func
        for uid, fname in data['func_blocks'].items():
            ret.function_blocks[uid] = fname
        return ret

    def _get_next_id(self) -> str:
        """Generate a unique object identifier and update diagram state."""
        ret = f"obj[{self._cid}]"
        self._cid += 1
        return ret

    def add_function(self, func: FBDFunc) -> str:
        """Adds a function to this diagram."""
        uid = self._get_next_id()
        self.function_blocks[uid] = func.name
        self._unique_functions[func.name] = func
        return uid

    def add_connection(self, src: str, dst: str) -> None:
        """
        Connect source (output) to destination (input).
        Both are specified as <function uid>.<variable name>.
        """
        srcf, srcv = _parse_var_ref(src)
        dstf, dstv = _parse_var_ref(dst)

        # following lines will cause errors if reference is invalid
        srcf_uid = self.function_blocks[srcf]
        dstf_uid = self.function_blocks[dstf]
        srcf_ref = self._unique_functions[srcf_uid]
        dstf_ref = self._unique_functions[dstf_uid]
        _ = srcf_ref.get_output_var(srcv)
        _ = dstf_ref.get_input_var(dstv)

        # if both references are valid, create a link
        self.connections[src] = dst

    def save(self, fname: str) -> None:
        """Utility function - store the diagram as file."""
        with open(fname, "w", encoding="utf-8") as file:
            json.dump(self.dump(), file, indent=1)

    @classmethod
    def from_file(cls, fname: str) -> "FBDiagram":
        """Utility function - load diagram from file."""
        with open(fname, "r", encoding="utf-8") as file:
            return cls.load(json.load(file))