"""
@what:  Container object for function data.
@why:   Function is the basic building block of an FBD.
@who:   TM
@when:  2022-03-04
"""

# internal
from pyfbd.variable import FBDVar
from pyfbd.fbdobj import FBDObj

def _check_vars(vars) -> None:
    """Raise error if any of the objects in supplied iterable is not a valid FBD variable."""
    for var in vars:
        if type(var) is not FBDVar:
            raise TypeError(f"Object {var} is not a valid FBD variable.")

class FBDFunc(FBDObj):
    """Basic building block of FBD. Represents a node in the functional graph."""
    DATAMODEL = ("name",)

    def __init__(self, name: str, inputs: "tuple[FBDVar]", outputs: "tuple[FBDVar]", state: "tuple[FBDVar]") -> None:
        _check_vars(inputs)
        _check_vars(outputs)
        _check_vars(state)
        self.name = name
        self.inputs = {inp.name: inp for inp in inputs}
        self.outputs = {out.name: out for out in outputs}
        self.state = {sta.name: sta for sta in state}

    def get_input_var(self, name: str) -> FBDVar:
        """Retrieve an input by name."""
        return self.inputs[name]

    def get_output_var(self, name: str) -> FBDVar:
        """Retrieve an output by name."""
        return self.outputs[name]

    def get_state_var(self, name: str) -> FBDVar:
        """Retrieve a state variable by name."""
        return self.state[name]

    def dump(self) -> dict:
        """Convert the data content of this class to dictionary."""
        ret = {key: self.__dict__[key] for key in FBDFunc.DATAMODEL}
        ret['inputs'] = [inp.dump() for _, inp in self.inputs.items()]
        ret['outputs'] = [out.dump() for _, out in self.outputs.items()]
        ret['state'] = [sta.dump() for _, sta in self.state.items()]
        return ret

    @staticmethod
    def load(data: dict) -> "FBDFunc":
        """Construct a class from data content."""
        inputs = tuple(FBDVar.load(inp) for inp in data['inputs'])
        outputs = tuple(FBDVar.load(out) for out in data['outputs'])
        state = tuple(FBDVar.load(sta) for sta in data['state'])
        return FBDFunc(data['name'], inputs, outputs, state)
