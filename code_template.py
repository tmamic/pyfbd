"""
@what:  Code template utilities for use in compiler extensions.
@why:   Maintain uniform template format, keep things extensible.
@who:   TM
@when:  2022-04-06
"""

# built-in
import re
from dataclasses import dataclass

@dataclass
class Section:
    """Keep track of section attributes."""
    name: str
    type: str
    properties: dict
    content: str

SECTION_REGEX = re.compile(r"<#(.*?):(.*)>")

def get_args(argstr: str) -> dict:
    """Parse a string of comma-separated arguments into key-value pairs."""
    ret = {}
    for pair in argstr.split(","):
        try:
            key, val = pair.split("=")
        except ValueError:
            key, val = pair, ""
        ret[key.strip()] = val.strip()
    return ret

def parse_section(sect: tuple) -> Section:
    """Parse section attributes."""
    stype, argstr = sect
    args = argstr.split(",")
    sname = args.pop(0).strip()
    props = {}
    while args:
        pair = args.pop(0)
        key, val = pair.split("=")
        props[key.strip()] = val.strip()
    return Section(sname, stype, props, "")

def iter_sections(text: str):
    """Iteratively returns section objects from a file segment."""
    for sect in re.findall(SECTION_REGEX, text):
        yield parse_section(sect)

def load_template(fname: str) -> dict:
    """Load a code template."""
    ret = {'fname': fname, 'sections': []}
    with open(fname, "r", encoding="utf-8") as template:
        for sect in iter_sections(template.read()):
            ret['sections'].append(sect)
    print(ret)
    return ret

TAG_REGEX = re.compile(r"<!(.*)>")
def _process_tag(match) -> str:
    """Utility function - convert regex match to tag string."""
    # group(1) is the first subgroup in TAG_REGEX, 0 is the entire match
    return match.group(1)

def fill_section(section: "list[str]", data: dict) -> str:
    """Parse the section for keys and fill them in with data."""
    return [re.sub(TAG_REGEX, lambda tag: str(data[_process_tag(tag)]), line) for line in section]