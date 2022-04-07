"""
@what:  Code template utilities for use in compiler extensions.
@why:   Maintain uniform template format, keep things extensible.
@who:   TM
@when:  2022-04-06
"""

# built-in
import json
import re

def load_template(fname: str) -> dict:
    """Load a json template. For now, don't do anything smart with it."""
    with open(fname, "r", encoding="utf-8") as template:
        return json.load(template)

TAG_REGEX = re.compile(r"<!(.*)>")
def _process_tag(match) -> str:
    """Utility function - convert regex match to tag string."""
    # group(1) is the first subgroup in TAG_REGEX, 0 is the entire match
    return match.group(1)

def fill_section(section: "list[str]", data: dict) -> str:
    """Parse the section lines for keys and fill them in with data."""
    return [re.sub(TAG_REGEX, lambda tag: str(data[_process_tag(tag)]), line) for line in section]