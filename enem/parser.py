def _fixed_value(line, start, size):
    """Helper function to find a value on a fixed size data"""

    start = start - 1
    end = start + size

    return line[start:end]

def parse_line(line):
    """
    Parses a line from the ENEM results file.
    See the LEIA-ME MICRODADDOS ENEM_2011.pdf, page 10, for more information.
    """

    try:
        result = dict()

        result["year"] = int(_fixed_value(line, 13, 4))
        result["school"] = int(_fixed_value(line, 204, 8))
        result["city"] = int(_fixed_value(line, 212, 7))
        result["city_name"] = _fixed_value(line, 219, 150).strip()
        result["state"] = _fixed_value(line, 369, 2).strip()

        result["nature_science_grade"] = float(_fixed_value(line, 537, 9))
        result["human_science_grade"] = float(_fixed_value(line, 546, 9))
        result["languages_grade"] = float(_fixed_value(line, 555, 9))
        result["math_grade"] = float(_fixed_value(line, 564, 9))

        return result
    except Exception:
        return None

def parse_file(file):
    """Parses a ENEM file."""
    for line in file:
        yield parse_line(line)
