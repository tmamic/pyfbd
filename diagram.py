"""
@what:  Container object for function block diagrams.
@why:   This is the object that we want to build in the end.
@who:   TM
@when:  2022-04-04
"""

class FBDiagram:
    """Data model of an FBD containing multiple functions and their interconnections."""

    def __init__(self) -> None:
        pass

    def dump(self) -> dict:
        """Convert diagram data to dictionary."""
        return {}

    @staticmethod
    def load(data: dict) -> "FBDiagram":
        """Construct diagram object from data."""
        return FBDiagram()