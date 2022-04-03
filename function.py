"""
@what:  Container object for function data.
@why:   Function is the basic building block of an FBD.
@who:   TM
@when:  2022-03-04
"""

# internal
from pyfbd.variable import FBDVar

class FBDFunc:
    """Basic building block of FBD. Represents a node in the functional graph."""

    def __init__(self, inputs: "tuple[FBDVar]", outputs: "tuple[FBDVar]", state: "tuple[FBDVar]") -> None:
        self.inputs = tuple((inp for inp in inputs))
        self.outputs = tuple((out for out in outputs))
        self.state = tuple((sta for sta in state))

    def dump(self) -> dict:
        """Convert the data content of this class to dictionary."""

    @staticmethod
    def load(data: dict) -> "FBDFunc":
        """Construct a class from data content."""