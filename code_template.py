"""
@what:  Code template utilities for use in compiler extensions.
@why:   Maintain uniform template format, keep things extensible.
@who:   TM
@when:  2022-04-06
"""

# built-in
import re
from dataclasses import dataclass

SECTION_REGEX = re.compile(r"<#(.*?):(.*)>")
SECT_END_REGEX = re.compile(r"<#end>")
VAR_REGEX = re.compile(r"<!(.*)>")

_debug = True

def _dbgprint(*pos, **kvpairs):
    """Debug print function."""
    if _debug:
        print(*pos, **kvpairs)

@dataclass
class Section:
    """Keep track of section attributes."""
    name: str
    type: str
    properties: dict
    content: str
    subsections: "list[Section]"

@dataclass
class Template:
    """Keep track of template attributes."""
    fname: str
    sections: "list[Section]"

def _parse_sect_header(segments: tuple) -> Section:
    """Create an incomplete section object with header data filled in."""
    # segments always have 2 items due to regex match form
    stype = segments[0]
    args = segments[1].split(",")
    if not args:
        raise ValueError("Missing section name.")
    sname = args[0]
    props = {}
    for prop in args[1:]:
        key, val = prop.split("=")
        props[key.strip()] = val.strip()
    return Section(sname, stype, props, "", [])

def _get_section_desc(line: str) -> Section:
    """Check if line contains valid section header and return section object if yes."""
    header = re.findall(SECTION_REGEX, line)
    if len(header) == 1:
        return _parse_sect_header(header[0])
    elif len(header) > 1:
        raise ValueError("Multiple header definitions in single line are not allowed.")
    # returning None signals that line contains no header

def load_template(fname: str) -> Template:
    """Parses a template from .fbdt file."""
    sections = []
    segstack = []
    last_sect = None
    with open(fname, "r", encoding="utf-8") as infile:
        for line in infile.readlines():
            sect = _get_section_desc(line)
            sect_end = re.search(SECT_END_REGEX, line)
            if sect:
                _dbgprint(f"[DBG] Entering section {sect.name} ({sect.type}).")
                sections.append(sect)
                if segstack:
                    # mark the subsection header location within containing section
                    segstack[-1].content += f"<!{sect.name}>"
                    segstack[-1].subsections.append(sect)
                segstack.append(sect)
            elif sect_end:
                last_sect = segstack.pop()
                _dbgprint(f"[DBG] Leaving section {last_sect.name} ({last_sect.type}).")
            elif segstack:
                segstack[-1].content += line
    if segstack:
        raise ValueError(f"Damaged sections: {[sc.name for sc in segstack]}. Last: {last_sect}.")

    ret = Template(fname, sections)
    return ret

def _match_finder(source: dict):
    """Generator for regex matching functions which replace keys by values of source."""
    def ret(match: re.Match) -> str:
        key = match.group(1)
        if key in source:
            _dbgprint(f"[DBG] Key '{key}' hit.")
            return str(source[key])
        return match.group(0)
    return ret

def fill_section(sect: Section, data: dict) -> bool:
    """Replace section tags with values of related keys in data. Return True if section is complete."""
    vars = set(re.findall(VAR_REGEX, sect.content))
    keys = set(data.keys())
    rem = vars.difference(keys)
    unused = keys.difference(vars)
    match_func = _match_finder(data)
    sect.content = re.sub(VAR_REGEX, match_func, sect.content)
    if unused:
        _dbgprint(f"[DBG] Unused keys: {unused}.")
    if rem:
        _dbgprint(f"[DBG] Remaining keys: {rem}.")
    else:
        _dbgprint(f"[DBG] Section {sect.name} complete.")
    return bool(rem)