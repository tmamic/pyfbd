"""
@what:  Container object for function block diagrams.
@why:   This is the object that we want to build in the end.
@who:   TM
@when:  2022-04-04
"""

# built-in
import json

# internal
from pyfbd.fbdobj import FBDObj
from pyfbd.function import FBDFunc

class FBDiagram(FBDObj):
    """Data model of an FBD containing multiple functions and their interconnections."""
    DATAMODEL = tuple()
    METADATA = ("_cid",)

    def __init__(self) -> None:
        self._cid = 0
        self._unique_functions = set()
        self.function_blocks = {}

    def dump(self) -> dict:
        """Convert diagram data to dictionary."""
        ret = {key: self.__dict__[key] for key in FBDiagram.DATAMODEL}
        ret['func_blocks'] = {uid: func.dump() for uid, func in self.function_blocks.items()}
        return ret

    def store(self) -> dict:
        """Store object with added metadata to dictionary. Prefered when saving state of instance."""
        ret = self.dump()
        ret.update({key: self.__dict__[key] for key in FBDiagram.METADATA})
        return ret

    @staticmethod
    def load(data: dict) -> "FBDiagram":
        """Construct diagram object from data."""
        ret = FBDiagram()
        for key in FBDiagram.DATAMODEL:
            # we are okay with keyerror here - datamodel must be complete
            ret.__dict__[key] = data[key]
        for key in FBDiagram.METADATA:
            # we are fine with metadata missing
            if key in data:
                ret.__dict__[key] = data[key]
        for uid, fdump in data['func_blocks'].items():
            ret.function_blocks[uid] = FBDFunc.load(fdump)
        return ret

    def _get_next_id(self) -> str:
        """Generate a unique object identifier and update diagram state."""
        ret = f"obj[{self._cid}]"
        self._cid += 1
        return ret

    def add_function(self, func: FBDFunc) -> str:
        """Adds a function to this diagram."""
        uid = self._get_next_id()
        self.function_blocks[uid] = func
        self._unique_functions.add(func)
        return uid

    def save(self, fname: str) -> None:
        """Utility function - store the diagram as file."""
        with open(fname, "w", encoding="utf-8") as file:
            json.dump(self.dump(), file, indent=1)

    @staticmethod
    def from_file(fname: str) -> "FBDiagram":
        """Utility function - load diagram from file."""
        with open(fname, "r", encoding="utf-8") as file:
            return FBDiagram.load(json.load(file))