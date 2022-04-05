"""
@what:  Container object for function block diagrams.
@why:   This is the object that we want to build in the end.
@who:   TM
@when:  2022-04-04
"""

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
        return ret

    def store(self) -> dict:
        """Store object with added metadata to dictionary. Prefered when saving state of instance."""
        ret = {key: self.__dict__[key] for key in FBDiagram.DATAMODEL}
        ret.update({key: self.__dict__[key] for key in FBDiagram.METADATA})
        return ret

    @staticmethod
    def load(data: dict) -> "FBDiagram":
        """Construct diagram object from data."""
        ret = FBDiagram()
        ret.__dict__.update(data)
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