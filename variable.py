"""
@what:  Container object for variable data.
@why:   Treat all variables inside an FBD equally.
@who:   TM
@when:  2022-03-04
"""

# built-in
import json

class FBDVar:
    """Variable descriptor class. Used to build data model of an FBD."""
    DATAMODEL = ("name", "type")

    def __init__(self, name: str, type: str) -> None:
        self.name = name
        self.type = type

    def dump(self) -> dict:
        """Convert the data content of this class to dictionary."""
        return {key: self.__dict__[key] for key in FBDVar.DATAMODEL}

    def __str__(self) -> str:
        return json.dumps(self.dump())

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, __o: object) -> bool:
        if type(__o) is not FBDVar:
            # we are type-racists here
            return False
        return hash(self) == hash(__o)

    @staticmethod
    def load(data: dict) -> "FBDVar":
        """Construct a class from data content."""
        return FBDVar(**data)