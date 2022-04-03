"""
@what:  Container object for function data.
@why:   Function is the basic building block of an FBD.
@who:   TM
@when:  2022-03-04
"""

# internal
from variable import FBDVar

def _check_vars(vars) -> None:
    """Raise error if any of the objects in supplied iterable is not a valid FBD variable."""
    for var in vars:
        if type(var) is not FBDVar:
            raise TypeError(f"Object {var} is not a valid FBD variable.")

class FBDFunc:
    """Basic building block of FBD. Represents a node in the functional graph."""

    def __init__(self, inputs: "tuple[FBDVar]", outputs: "tuple[FBDVar]", state: "tuple[FBDVar]") -> None:
        _check_vars(inputs)
        _check_vars(outputs)
        _check_vars(state)
        self.inputs = tuple((inp for inp in inputs))
        self.outputs = tuple((out for out in outputs))
        self.state = tuple((sta for sta in state))

    def dump(self) -> dict:
        """Convert the data content of this class to dictionary."""

    @staticmethod
    def load(data: dict) -> "FBDFunc":
        """Construct a class from data content."""