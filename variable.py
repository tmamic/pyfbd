"""
@what:  Container object for variable data.
@why:   Treat all variables inside an FBD equally.
@who:   TM
@when:  2022-03-04
"""

class FBDVar:
    """Variable descriptor class. Used to build data model of an FBD."""
    DATAMODEL = ("name", "type", "inival", "val")

    def __init__(self, name: str, type: str, inival, **metadata) -> None:
        self.name = name
        self.type = type
        self.val = inival
        self.inival = inival

    def dump(self) -> dict:
        """Convert the data content of this class to dictionary."""
        return {key: self.__dict__[key] for key in FBDVar.DATAMODEL}

    @staticmethod
    def load(data: dict) -> "FBDVar":
        """Construct a class from data content."""
        return FBDVar(**data)