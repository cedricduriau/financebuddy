# stdlib
import hashlib
import re

REGEX_WHITESPACE = re.compile(r"\s+")


def remove_whitespace(s: str) -> str:
    result = re.sub(REGEX_WHITESPACE, "", s)
    return result


def remove_plus(s: str) -> str:
    result = s.replace("+", "")
    return result


def sanitize_value_string(s: str) -> str:
    result = remove_whitespace(s)
    result = remove_plus(result)

    dot_pos = result.rfind(".")
    comma_pos = result.rfind(",")
    if comma_pos > dot_pos:
        result = result.replace(".", "")
        result = result.replace(",", ".")
    else:
        result = result.replace(",", "")
    return result


def hash_string(s: str) -> str:
    h = hashlib.md5(s.encode("utf-8")).hexdigest()
    return h
