"""
@what:  Basic object from which elements of FBD inherit some common functions.
@why:   There are some generalizable things we want to do at all levels of the hierarchy.
@who:   TM
@when:  2022-04-04
"""

# built-in
import json

class FBDObj:
    """Shared stuff between all elements of FBD."""

    def __str__(self) -> str:
        return json.dumps(self.dump())

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, __o: object) -> bool:
        if type(__o) is not type(self):
            # we are type-racists here
            return False
        return hash(self) == hash(__o)