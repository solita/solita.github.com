import re


def filename_starts_with_a_date(filename: str) -> list[str]:
    if not re.search('^[0-9]{4}-[0-9]{2}-[0-9]{2}', filename):
        return ['Filename must start with a date']

    return []
